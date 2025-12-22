from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rdmo.config.helpers import DeclaredPlugin
from rdmo.config.legacy import get_plugins_from_legacy_settings
from rdmo.config.models import Plugin
from rdmo.config.plugin_resolver import (
    get_plugins_from_settings,
)


def save_declared_plugin(declared: DeclaredPlugin, *, replace: bool, dry_run: bool) -> str:
    uri_prefix = declared.uri_prefix or getattr(settings, "DEFAULT_URI_PREFIX", None)
    if not uri_prefix:
        raise CommandError("No uri_prefix available (neither provided nor DEFAULT_URI_PREFIX).")

    uri_path = declared.uri_path or declared.url_name

    try:
        plugin = Plugin.objects.get(uri_prefix=uri_prefix, uri_path=uri_path)
        exists = True
        if not replace:
            return f"skipped(exists): {plugin.python_path} -> {plugin.uri}"
    except Plugin.DoesNotExist:
        plugin = Plugin(uri_prefix=uri_prefix, uri_path=uri_path)
        exists = False

    plugin.title_lang1 = declared.title
    plugin.python_path = declared.python_path
    if declared.url_name is not None:
        plugin.url_name = declared.url_name
    plugin.available = True

    action = "replaced" if (exists and replace) else ("created" if not exists else "updated")
    if dry_run:
        uri = f"{uri_prefix}/plugins/{uri_path}"
        return f"{action} (dry-run): {declared.python_path} -> {uri}"

    plugin.full_clean()
    plugin.save()
    return f"{action}: {plugin.python_path} from {declared.source}-> {plugin.uri}"


def merge_legacy_and_current_plugins(
        legacy: list[DeclaredPlugin], modern: list[DeclaredPlugin]
    ) -> list[DeclaredPlugin]:
    legacy_uri_paths = {d.uri_path for d in legacy}
    legacy_paths = {d.python_path for d in legacy}
    filtered_modern = [
        i for i in modern
        if i.uri_path not in legacy_uri_paths and i.python_path not in legacy_paths
    ]
    return legacy + filtered_modern


class Command(BaseCommand):
    help = _("Create or update Plugin objects from PLUGINS, legacy settings. Can also clear all plugins.")

    def add_arguments(self, parser):
        parser.add_argument(
            "--from-settings",
            action="store_true",
            help=_("Import Plugins from legacy settings and current settings.PLUGINS."),
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help=_("Replace existing rows instead of updating Plugin objects."),
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help=_("Do not write to the database, only print intended actions."),
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help=_("Delete ALL existing Plugin objects before importing."),
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help=_("Do not prompt for confirmation when using --clear."),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        from_settings_flag: bool = options["from_settings"]
        replace: bool = options["replace"]
        dry_run: bool = options["dry_run"]
        do_clear: bool = options["clear"]
        force: bool = options["force"]

        declared_plugins: list[DeclaredPlugin] = []

        # Optional destructive phase first
        if do_clear:
            self.stdout.write(self.style.WARNING("⚠ --clear requested: ALL Plugin objects will be removed."))
            self.clear_all_plugins(dry_run=dry_run, force=force)

        # Collect plugin declarations
        if from_settings_flag:
            legacy_plugins = get_plugins_from_legacy_settings()
            plugins = get_plugins_from_settings()
            declared_plugins.extend(
                merge_legacy_and_current_plugins(legacy_plugins, plugins)  # prioritize legacy, skip duplicates
            )

        # If no import source and only --clear, we are done.
        if not declared_plugins:
            if do_clear:
                # never raise on dry-run; just say we are done.
                msg = "✔ clear completed (dry-run; no changes committed)." if dry_run else "✔ clear completed."
                self.stdout.write(self.style.SUCCESS(msg))
                return
            raise CommandError(
                "Nothing to do. Use --clear and/or --from-settings."
            )

        if from_settings_flag:
            self.stdout.write(self.style.WARNING(
                "Reading legacy plugin settings. These are deprecated and will be removed in a future release."
            ))

        # Deterministic order for output
        declared_plugins.sort(key=lambda x: (x.python_path, x.uri_path or ""))

        # -------------------- import validation --------------------------
        errors: list[tuple[DeclaredPlugin, Exception]] = []
        for d in declared_plugins:
            try:
                import_string(d.python_path)
            except Exception as exc:
                errors.append((d, exc))
                self.stdout.write(self.style.ERROR(f"✖ import FAILED: {d.python_path} ({exc})"))

        if errors:
            msg = f"{len(errors)} plugin(s) failed import validation; aborting before database changes."
            for error in errors:
                msg += f"\n- {error[0]}\n\t{error[1]}"

            if dry_run:
                # In dry-run mode, never raise: just report and exit
                self.stdout.write(self.style.WARNING(msg))
                self.stdout.write(self.style.SUCCESS("✔ dry-run complete; no changes committed."))
                return
            # Non-dry-run: keep strict behaviour
            raise CommandError(msg)

        results: list[str] = []
        for d in declared_plugins:
            try:
                msg = save_declared_plugin(d, replace=replace, dry_run=dry_run)
                results.append(self.style.SUCCESS(f"✔ {msg}"))
            except Exception as exc:
                results.append(self.style.ERROR(f"✖ {d.python_path} failed: {exc}"))

        for line in results:
            self.stdout.write(line)

        if dry_run:
            self.stdout.write(self.style.SUCCESS("✔ dry-run complete; no changes committed."))
            return

    def clear_all_plugins(self, dry_run: bool, force: bool) -> None:
        """
        Clear all Plugin rows. In dry-run, print what would be deleted.
        Without --force (and not dry-run), prompt for confirmation.
        """
        queryset = Plugin.objects.all().order_by("uri_prefix", "uri_path")

        if not queryset.exists():
            self.stdout.write(self.style.WARNING("⚠ no Plugin objects found; nothing to clear."))
            return

        self.stdout.write(self.style.WARNING(f"⚠ about to clear {queryset.count()} Plugin object(s):"))
        for p in queryset:
            if dry_run:
                self.stdout.write(self.style.WARNING(f"• {p.python_path} at {p.uri} will be deleted"))
            else:
                self.stdout.write(self.style.WARNING(f"• {p.python_path} at {p.uri} marked for deletion"))

        if dry_run:
            return

        if not force:
            self.stdout.write("")
            self.stdout.write(self.style.WARNING("Type 'yes' to confirm deletion of ALL Plugin objects: "), ending="")
            try:
                confirm = input().strip().lower()
            except EOFError:
                confirm = ""
            if confirm != "yes":
                raise CommandError("Clear aborted by user.")

        deleted, _ = queryset.delete()
        self.stdout.write(self.style.SUCCESS(f"✔ deleted {deleted} object(s)."))
