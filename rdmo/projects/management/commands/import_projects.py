from __future__ import annotations

import logging
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from rdmo.accounts.utils import find_user
from rdmo.core.plugins import get_plugin

from .utils import FakeRequest

logger = logging.getLogger(__name__)


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
        --include-memberships --create-new-users --format madmp --as-user admin
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
            "--include-memberships",
            action="store_true",
            help="Read the memberships from the xml and recreate memberships."
        )
        parser.add_argument(
            "--create-new-users",
            action="store_true",
            help="When importing members, auto-create missing users. "
                 "Default is to only use existing users (error if missing)."
        )
        parser.add_argument(
            "--as-user-id",
            type=int,
            metavar="USER",
            help="Pretend the import is executed by this user (id). "
                 "Defaults to the first superuser."
        )
        parser.add_argument(
            "--as-username",
            metavar="USERNAME",
            help="Pretend the import is executed by this user (username). "
                 "Defaults to the first superuser."
        )

    def handle(self, *args, **options):
        import_format = options["format"]
        base_dir = Path(options["dir"]).expanduser().resolve()
        explicit_files = options.get("files")
        include_memberships = options["include_memberships"]
        create_new_users = options["create_new_users"]
        as_user_id = options.get("as_user_id")
        as_username = options.get("as_username")
        project_ids = sorted(set(options.get("projects") or []))

        # sanity-check plugin key
        if get_plugin("PROJECT_IMPORTS", import_format) is None:
            raise CommandError(
                f'Import format "{import_format}" is not configured. '
                "Check your ``PROJECT_IMPORTS`` setting."
            )

        # 1) collect xml files (from --files OR by scanning --dir)
        xml_files = self._collect_xml_files(explicit_files, base_dir, project_ids)
        if not xml_files:
            self.stdout.write(self.style.WARNING("No XML files to import."))
            return

        failures = []

        # 2) import each file in its own transaction

        # need to get a user and a fake request for when the plugin calls self.request.user
        user = find_user(user_id=as_user_id, username=as_username)
        if user is None:
            user = get_user_model().objects.filter(is_superuser=True).first()
        fake_request = FakeRequest(user)

        for xml_file in xml_files:
            self.stdout.write(f"→ Importing {xml_file}")
            try:
                with transaction.atomic():
                    plugin = get_plugin("PROJECT_IMPORTS", import_format)
                    plugin.file_name = str(xml_file)
                    plugin.request = fake_request
                    plugin.current_project = None
                    project = plugin.import_to_project(
                        include_memberships=include_memberships,
                        allow_creation_of_new_users=create_new_users,
                    )

                self.stdout.write(
                    self.style.SUCCESS(f'   ✓ Project {project.pk} "{project.title}" imported successfully.')
                )
            except CommandError as exc:
                logger.exception("Import failed for %s", xml_file)
                self.stdout.write(self.style.ERROR(f"   ✗ {exc} (see log)"))
                failures.append((xml_file, str(exc)))
            except Exception as exc:
                logger.exception("Unexpected error importing %s", xml_file)
                self.stdout.write(self.style.ERROR(f"   ✗ {exc} (see log)"))
                failures.append((xml_file, str(exc)))

        if failures:
            self.stdout.write(self.style.WARNING("\nImport finished with errors:"))
            for path, msg in failures:
                self.stdout.write(f"  • {path}: {msg}")
            self.stdout.write("")  # final newline

    def _collect_xml_files(self, explicit_files, base_dir, project_ids):
        """Return a list of XML Paths based on --files or scanning --dir."""
        if explicit_files:
            return self._resolve_explicit_files(explicit_files)

        base_path = Path(base_dir).expanduser().resolve()
        if not base_path.is_dir():
            raise CommandError(f'Dir "{base_path}" does not exist or is not a directory.')

        return self._scan_export_dir(base_path, project_ids)

    def _resolve_explicit_files(self, files):
        """Validate explicit --files and return resolved Paths."""
        xml_files = []
        for file_str in files:
            path = Path(file_str).expanduser().resolve()
            if not path.is_file():
                raise CommandError(f'File "{path}" does not exist or is not a file.')
            if path.suffix.lower() != ".xml":
                self.stdout.write(self.style.WARNING(f'   • Skipping non-XML file "{path.name}".'))
                continue
            xml_files.append(path)
        return xml_files

    def _scan_export_dir(self, base_path, project_ids):
        """
        Walk the export directory layout and pick one XML per numeric project folder.
        Skips known non-project subfolders like "answers" and "views".
        """
        xml_files = []
        projects_found = set()

        for project_dir in sorted(base_path.iterdir(), key=lambda p: p.name):
            if not project_dir.is_dir():
                continue
            if project_dir.name in ("answers", "views"):
                continue  # not project folders

            try:
                dir_id = int(project_dir.name)
            except ValueError:
                self.stdout.write(self.style.WARNING(f'Skip "{project_dir.name}", folder name is not a number.'))
                continue

            if project_ids and dir_id not in project_ids:
                continue

            xml_path = self._pick_project_xml(project_dir)
            if xml_path:
                xml_files.append(xml_path)
                projects_found.add(dir_id)

        missing_project_ids = set(project_ids) - projects_found
        if project_ids and missing_project_ids:
            self.stdout.write(self.style.WARNING(f"Some projects could not be found {missing_project_ids}."))

        return xml_files

    def _pick_project_xml(self, project_dir):
        """
        Choose a single XML deterministically from a project folder.
        Warns when none or multiple are present.
        """
        candidates = sorted(project_dir.glob("*.xml"))
        if not candidates:
            self.stdout.write(self.style.WARNING(f'No XML file found in "{project_dir}".'))
            return None
        if len(candidates) > 1:
            chosen = candidates[0]
            names = ", ".join(p.name for p in candidates[:3])
            more = "" if len(candidates) <= 3 else f" (+{len(candidates) - 3} more)"
            self.stdout.write(
                self.style.WARNING(
                    f'Multiple XML files in "{project_dir.name}" [{names}{more}], using "{chosen.name}".'
                )
            )
            return chosen
        return candidates[0]
