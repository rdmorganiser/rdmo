from __future__ import annotations

import json
import logging
from collections.abc import Iterable
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from rdmo.core.plugins import get_plugin
from rdmo.projects.models import Membership, Project
from rdmo.projects.utils import (
    save_import_snapshot_values,
    save_import_tasks,
    save_import_values,
    save_import_views,
)

from .utils import FakeRequest, get_cli_user, make_unique_username

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    """
    Import projects that were previously exported via ``export_projects``.
    The command expects the directory structure created by the export
    (each project in a numbered sub-folder containing one ``*.xml`` file
    and optionally a ``members.json``).

    Examples
    --------
    # import everything that is inside ./exports
    $ python manage.py import_projects

    # only import projects 2 and 5, create memberships, use a custom plugin
    $ python manage.py import_projects --projects 2 5 --with-members --format madmp
    """

    # ---------------------------------------------------------------------
    # CLI argument definitions
    # ---------------------------------------------------------------------
    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            metavar="DIR",
            default="exports",
            help="Directory with exported project sub-folders (default: exports/).",
        )
        parser.add_argument(
            "--projects",
            nargs="*",
            type=int,
            metavar="ID",
            help="Only import the listed project-ID folders.",
        )
        parser.add_argument(
            "--format",
            default="xml",
            help="Import plugin key to use (must be configured in ``settings.PROJECT_IMPORTS``).",
        )
        parser.add_argument(
            "--with-members",
            action="store_true",
            help="Also read a companion ``members.json`` and recreate memberships.",
        )
        parser.add_argument(
            "--as-user",
            metavar="USER",
            help="Pretend the import is executed by this user (pk or username). "
            "Defaults to the first superuser.",
        )

    # ---------------------------------------------------------------------
    # main entry point
    # ---------------------------------------------------------------------
    def handle(self, *args, **options):
        base_path = Path(options["path"]).expanduser().resolve()
        if not base_path.is_dir():
            raise CommandError(
                f'Path "{base_path}" does not exist or is not a directory.'
            )

        project_filter: set[int] | None = (
            set(options["projects"]) if options.get("projects") else None
        )
        plugin_key: str = options["format"]
        import_members: bool = options["with_members"]
        self.import_user = get_cli_user(options.get("as_user"))

        # sanity-check plugin key
        if get_plugin("PROJECT_IMPORTS", plugin_key) is None:
            raise CommandError(
                f'Import format "{plugin_key}" is not configured. '
                "Check your ``PROJECT_IMPORTS`` setting."
            )

        failures: list[tuple[Path, str]] = []

        # iterate over sub-folders --------------------------------------------------
        for project_dir in sorted(base_path.iterdir(), key=lambda p: p.name):
            if not project_dir.is_dir():
                continue

            try:
                dir_id = int(project_dir.name)
            except ValueError:
                self.stdout.write(
                    self.style.WARNING(
                        f'Skip "{project_dir.name}", folder name is not a number.'
                    )
                )
                continue

            if project_filter and dir_id not in project_filter:
                continue

            # each sub-folder *must* contain exactly one XML file ------------------
            xml_candidates = list(project_dir.glob("*.xml"))
            if not xml_candidates:
                self.stdout.write(
                    self.style.WARNING(f'No XML file found in "{project_dir}".')
                )
                continue

            xml_file = xml_candidates[0]
            self.stdout.write(f"→ Importing {xml_file.relative_to(base_path)}")

            try:
                with transaction.atomic():
                    project = self._import_single_project(xml_file, plugin_key)
                    if import_members:
                        self._import_members(project, project_dir / "members.json")

                self.stdout.write(
                    self.style.SUCCESS(
                        f'   ✓ Project {project.pk} "{project.title}" imported successfully.'
                    )
                )
            except CommandError as exc:  # expected / user-facing
                logger.exception("Import failed for %s", xml_file)
                self.stdout.write(self.style.ERROR(f"   ✗ {exc} (see log)"))
                failures.append((xml_file.relative_to(base_path), str(exc)))
                continue
            except Exception as exc:
                # unexpected; cancel this project but keep processing others
                logger.exception("Import failed for %s", xml_file)
                self.stdout.write(self.style.ERROR(f"   ✗ {exc} (see log)"))
                failures.append((xml_file.relative_to(base_path), str(exc)))
                raise

        if failures:
            self.stdout.write(self.style.NOTICE("\nImport finished with errors:"))
            for path, msg in failures:
                self.stdout.write(f"  • {path}: {msg}")
            self.stdout.write("")  # final newline for readability

    # ---------------------------------------------------------------------
    # helpers
    # ---------------------------------------------------------------------
    def _import_single_project(self, xml_file: Path, plugin_key: str) -> Project:
        """Run the configured import plugin and persist project + values."""
        # fresh plugin instance each time
        plugin = get_plugin("PROJECT_IMPORTS", plugin_key)
        plugin.file_name = str(xml_file)
        plugin.request = FakeRequest(self.import_user)  # CLI → Fake HTTP request
        plugin.current_project = None  # always *create* a new project

        if not plugin.check():
            raise CommandError(
                f'Plugin "{plugin_key}" rejected file "{xml_file.name}".'
            )

        plugin.process()

        for val in plugin.values:
            val.current = None
        for snap in plugin.snapshots:
            for val in snap.snapshot_values:
                val.current = None

        project: Project = plugin.project
        if project.pk is None:  # ensure object is saved before M2M relations
            project.site = Site.objects.get_current()
            project.save()

        # -----------------------------------------------------------------
        # build “checked” sets so that *all* answers / snapshots are imported
        # (the utils functions only import rows that we explicitly mark)
        # -----------------------------------------------------------------
        checked_values: set[str] = {
            f"{v.attribute.uri}[{v.set_prefix}][{v.set_index}][{v.collection_index}]"
            for v in plugin.values
            if v.attribute
        }

        checked_snapshots: set[str] = set()
        for snapshot in plugin.snapshots:
            checked_snapshots.update(
                f"{val.attribute.uri}[{snapshot.snapshot_index}][{val.set_prefix}][{val.set_index}][{val.collection_index}]"
                for val in snapshot.snapshot_values
                if val.attribute
            )

        # persist everything ------------------------------------------------
        save_import_values(project, plugin.values, checked_values)
        save_import_snapshot_values(project, plugin.snapshots, checked_snapshots)
        save_import_tasks(project, plugin.tasks)
        save_import_views(project, plugin.views)

        return project

    # ---------------------------------------------------------------------
    # optional membership import
    # ---------------------------------------------------------------------
    def _import_members(self, project: Project, members_json: Path) -> None:
        if not members_json.is_file():
            self.stdout.write(
                self.style.WARNING(
                    "   ↺ No members.json present, skipping memberships."
                )
            )
            return

        try:
            payload: Iterable[dict] = json.loads(
                members_json.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError) as exc:
            raise CommandError(f"Failed to read {members_json}: {exc}") from exc

        created, skipped = 0, 0
        for record in payload:

            email = (record.get("email") or "").lower()
            user = None

            if email:
                user = User.objects.filter(email__iexact=email).first()

            if not user and email:
                # choose seed: provided username or local-part of e-mail
                desired = record.get("username") or email.split("@")[0]

                username = make_unique_username(desired)

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=record.get("first_name", ""),
                    last_name=record.get("last_name", ""),
                    is_active=True,
                )
                user.set_unusable_password()
                user.save(update_fields=["password"])

                if username != desired:
                    logger.info(
                        "Username '%s' already taken, auto-created unique name '%s'.",
                        desired,
                        username,
                    )

            if user is None:
                skipped += 1
                self.stdout.write(
                    self.style.WARNING(f"   ↺ No user for {record!r}, skipping.")
                )
                continue

            role = record.get("role") or "guest"
            try:
                Membership.objects.update_or_create(
                    project=project, user=user, defaults={"role": role}
                )
            except IntegrityError as exc:
                logger.warning(
                    "   ↺ Duplicate membership %s / %s: %s", project.pk, user.pk, exc
                )
                skipped += 1
            else:
                self.stdout.write(f'      • added "{user.username}" as {role}')
                created += 1

        if created:
            logger.info("Added %d membership(s) to project %s", created, project.pk)
        if skipped:
            logger.info(
                "Skipped %d membership record(s) for project %s", skipped, project.pk
            )
