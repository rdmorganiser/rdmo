from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from rdmo.config.legacy import get_plugins_from_legacy_settings
from rdmo.config.models import Plugin
from rdmo.config.serializers.v1 import PluginSerializer
from rdmo.config.utils import get_plugins_from_settings
from rdmo.core.utils import get_languages


def _ensure_plugin_meta(plugin: Plugin, plugin_class, *, dry_run: bool) -> str | None:
    if plugin.plugin_meta:
        return None

    if dry_run:
        return "would refresh plugin_meta"

    plugin.plugin_meta = plugin.build_plugin_meta(plugin_class)
    plugin.save(update_fields=['plugin_meta'])
    return "refreshed plugin_meta"


def _validate_declared_plugin(plugin: Plugin | None, declared: dict) -> None:
    python_path = declared.get('python_path')
    restore_plugins = None
    if python_path and python_path not in settings.PLUGINS:
        restore_plugins = list(settings.PLUGINS)
        settings.PLUGINS = [*restore_plugins, python_path]

    serializer_data = {
        'uri_prefix': declared.get('uri_prefix'),
        'uri_path': declared.get('uri_path'),
        'python_path': declared.get('python_path'),
        'url_name': declared.get('url_name'),
        'available': declared.get('available', True),
    }
    if declared.get('title'):
        languages = get_languages()
        if languages:
            serializer_data[f"title_{languages[0][0]}"] = declared.get('title')
    serializer_data = {key: value for key, value in serializer_data.items() if value is not None}
    serializer = PluginSerializer(instance=plugin, data=serializer_data, partial=True)

    if python_path and python_path not in serializer.fields['python_path'].choices:
        serializer.fields['python_path'].choices = [
            *serializer.fields['python_path'].choices,
            python_path,
        ]

    try:
        serializer.is_valid(raise_exception=True)
    except RestFrameworkValidationError as exc:
        messages = []
        for field, errors in exc.detail.items():
            for error in errors:
                messages.append(f"{field}: {error}")
        raise CommandError("Validation failed: " + "; ".join(messages)) from exc
    finally:
        if restore_plugins is not None:
            settings.PLUGINS = restore_plugins

def save_declared_plugin(declared: dict, *, replace: bool, dry_run: bool) -> str:
    uri_prefix = declared["uri_prefix"] or getattr(settings, "DEFAULT_URI_PREFIX", None)
    if not uri_prefix:
        raise CommandError("No uri_prefix available (neither provided nor DEFAULT_URI_PREFIX).")

    uri_path = declared["uri_path"] or declared["url_name"]

    try:
        plugin = Plugin.objects.get(uri_prefix=uri_prefix, uri_path=uri_path)
        exists = True
        if not replace:
            try:
                plugin_class = import_string(plugin.python_path)
            except ImportError:
                return f"skipped(exists): {plugin.python_path} -> {plugin.uri}"

            refresh_msg = _ensure_plugin_meta(plugin, plugin_class, dry_run=dry_run)
            if refresh_msg:
                return f"skipped(exists, {refresh_msg}): {plugin.python_path} -> {plugin.uri}"
            return f"skipped(exists): {plugin.python_path} -> {plugin.uri}"
    except Plugin.DoesNotExist:
        plugin = Plugin(uri_prefix=uri_prefix, uri_path=uri_path)
        exists = False

    plugin.title_lang1 = declared["title"]
    plugin.python_path = declared["python_path"]
    if declared["url_name"] is not None:
        plugin.url_name = declared["url_name"]
    plugin.available = True

    _validate_declared_plugin(plugin, declared)

    action = "replaced" if (exists and replace) else ("created" if not exists else "updated")
    if dry_run:
        uri = f"{uri_prefix}/plugins/{uri_path}"
        return f"{action} (dry-run): {declared['python_path']} -> {uri}"

    plugin.full_clean()
    plugin.save()
    if settings.MULTISITE:
        current_site = Site.objects.get_current()
        plugin.editors.set([current_site])
        plugin.sites.set([current_site])

    return f"{action}: {plugin.python_path} -> {plugin.uri}"


def merge_legacy_and_current_plugins(
        legacy_plugins: list[dict], plugins: list[dict]
    ) -> list[dict]:
    legacy_uri_paths = {d['uri_path'] for d in legacy_plugins}
    legacy_paths = {d['python_path'] for d in legacy_plugins}
    filtered_plugins = [
        i for i in plugins
        if i['uri_path'] not in legacy_uri_paths and i['python_path'] not in legacy_paths
    ]
    return legacy_plugins + filtered_plugins


class Command(BaseCommand):
    help = _("Create or update Plugin objects from PLUGINS, legacy settings. Can also clear all plugins.")

    def add_arguments(self, parser):
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
        # Optional destructive phase first
        if options["clear"]:
            self.stdout.write(self.style.WARNING("⚠ --clear requested: ALL Plugin objects will be removed."))
            self.clear_all_plugins(dry_run=options["dry_run"], force=options["force"])

        # Collect plugin declarations
        plugins_from_settings: list[dict] = []

        legacy_plugins = get_plugins_from_legacy_settings()
        try:
            plugins = get_plugins_from_settings()
        except ValidationError as e:
            raise CommandError("\n".join(e.messages)) from e

        plugins_from_settings.extend(
            merge_legacy_and_current_plugins(legacy_plugins, plugins)  # prioritize legacy, skip duplicates
        )

        # If no import source and only --clear, we are done.
        if not plugins_from_settings:
            if options["clear"]:
                # never raise on dry-run; just say we are done.
                if options["dry_run"]:
                    self.stdout.write(self.style.SUCCESS("✔ clear completed (dry-run; no changes committed)."))
                else:
                    self.stdout.write(self.style.SUCCESS("✔ clear completed."))
                return
            raise CommandError(
                "Nothing to do."
            )

        self.stdout.write(self.style.WARNING(
            "Reading legacy plugin settings. These are deprecated and will be removed in a future release."
        ))

        # Deterministic order for output
        plugins_from_settings.sort(key=lambda x: (x["python_path"], x["uri_path"] or ""))

        # -------------------- import validation --------------------------
        errors: list[tuple[dict, Exception]] = []
        for plugin in plugins_from_settings:
            try:
                import_string(plugin["python_path"])
            except ImportError as exc:
                errors.append((plugin, exc))
                self.stdout.write(self.style.ERROR(f"✖ import FAILED: {plugin['python_path']} ({exc})"))

        if errors:
            msg = f"{len(errors)} plugin(s) failed import validation; aborting before database changes."
            for error in errors:
                msg += f"\n- {error[0]}\n\t{error[1]}"

            if options["dry_run"]:
                # In dry-run mode, never raise: just report and exit
                self.stdout.write(self.style.WARNING(msg))
                self.stdout.write(self.style.SUCCESS("✔ dry-run complete; no changes committed."))
                return
            # Non-dry-run: keep strict behaviour
            raise CommandError(msg)

        results: list[str] = []
        for plugin in plugins_from_settings:
            try:
                msg = save_declared_plugin(plugin, replace=options["replace"], dry_run=options["dry_run"])
                results.append(self.style.SUCCESS(f"✔ {msg}"))
            except CommandError as exc:
                results.append(self.style.ERROR(f"✖ {plugin['python_path']} failed: {exc}"))

        for line in results:
            self.stdout.write(line)

        if options["dry_run"]:
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
