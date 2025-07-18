from __future__ import annotations

import json
import logging
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from rdmo.core.plugins import get_plugin
from rdmo.projects.utils import import_memberships

from .utils import FakeRequest, get_cli_user

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    """
    Import projects that were previously exported via ``export_projects``.
    You may either point to a directory of exported sub-folders, or
    explicitly list XML file paths.

    Examples
    --------
    # import all projects inside ./exports
    $ python manage.py import_projects

    # import only project folders 2 and 5
    $ python manage.py import_projects --dir ./exports --projects 2 5

    # import specific XML files directly
    $ python manage.py import_projects --files /tmp/p1.xml /tmp/p2.xml

    # import with memberships and custom plugin
    $ python manage.py import_projects --files /tmp/p1.xml \
        --with-members --format madmp --as-user admin
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            metavar="DIR",
            default="exports",
            help="Directory with exported project sub-folders (default: exports/)."
        )
        parser.add_argument(
            "--files",
            nargs="*",
            type=str,
            metavar="XML",
            help="Explicit paths to XML files to import."
        )
        parser.add_argument(
            "--projects",
            nargs="*",
            type=int,
            metavar="ID",
            help="Only import the listed project-ID folders (when using --dir)."
        )
        parser.add_argument(
            "--format",
            default="xml",
            help="Import plugin key to use (must be configured in ``settings.PROJECT_IMPORTS``)."
        )
        parser.add_argument(
            "--with-members",
            action="store_true",
            help="Also read a companion ``members.json`` and recreate memberships."
        )
        parser.add_argument(
            "--allow-new-users",
            action="store_true",
            help="When importing members, auto-create missing users. "
                 "Default is to only use existing users (error if missing)."
        )
        parser.add_argument(
            "--as-user",
            metavar="USER",
            help="Pretend the import is executed by this user (pk or username). "
                 "Defaults to the first superuser."
        )

    def handle(self, *args, **options):
        plugin_key = options["format"]
        import_members = options["with_members"]
        create_users = options["allow_new_users"]
        self.import_user = get_cli_user(options.get("as_user"))

        # sanity-check plugin key
        if get_plugin("PROJECT_IMPORTS", plugin_key) is None:
            raise CommandError(
                f'Import format "{plugin_key}" is not configured. '
                "Check your ``PROJECT_IMPORTS`` setting."
            )

        xml_files: list[Path] = []
        explicit = options.get("files")
        if explicit:
            # Use explicitly provided XML file paths
            for file_str in explicit:
                xml_file = Path(file_str).expanduser().resolve()
                if not xml_file.is_file():
                    raise CommandError(f'File "{xml_file}" does not exist or is not a file.')
                xml_files.append(xml_file)
        else:
            # Scan a directory of numbered subfolders
            base_path = Path(options["dir"]).expanduser().resolve()
            if not base_path.is_dir():
                raise CommandError(f'Dir "{base_path}" does not exist or is not a directory.')

            project_filter: set[int] | None = (
                set(options["projects"]) if options.get("projects") else None
            )

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

                xml_candidates = list(project_dir.glob("*.xml"))
                if not xml_candidates:
                    self.stdout.write(
                        self.style.WARNING(f'No XML file found in "{project_dir}".')
                    )
                    continue

                xml_files.append(xml_candidates[0])

        if not xml_files:
            self.stdout.write(self.style.WARNING("No XML files to import."))
            return

        failures: list[tuple[Path, str]] = []

        for xml_file in xml_files:
            self.stdout.write(f"→ Importing {xml_file}")
            try:
                with transaction.atomic():
                    plugin = get_plugin("PROJECT_IMPORTS", plugin_key)
                    plugin.file_name = str(xml_file)
                    plugin.request = FakeRequest(self.import_user)
                    plugin.current_project = None

                    project = plugin.import_to_project()

                    if import_members:
                        members_path = xml_file.parent / "members.json"
                        if not members_path.is_file():
                            raise CommandError(f"No members.json alongside {xml_file.name}")
                        data = json.loads(members_path.read_text(encoding="utf-8"))
                        try:
                            created, skipped = import_memberships(project, data, create_users=create_users)
                        except ValidationError as exc:
                            raise CommandError(str(exc)) from exc
                        self.stdout.write(self.style.SUCCESS(f"   ✓ {created} memberships added, {skipped} skipped."))

                self.stdout.write(
                    self.style.SUCCESS(
                        f'   ✓ Project {project.pk} "{project.title}" imported successfully.'
                    )
                )
            except CommandError as exc:
                logger.exception("Import failed for %s", xml_file)
                self.stdout.write(self.style.ERROR(f"   ✗ {exc} (see log)"))
                failures.append((xml_file, str(exc)))
            except Exception as exc:
                # unexpected; cancel this project but continue others
                logger.exception("Unexpected error importing %s", xml_file)
                self.stdout.write(self.style.ERROR(f"   ✗ {exc} (see log)"))
                failures.append((xml_file, str(exc)))

        if failures:
            self.stdout.write(self.style.NOTICE("\nImport finished with errors:"))
            for path, msg in failures:
                self.stdout.write(f"  • {path}: {msg}")
            self.stdout.write("")  # final newline
