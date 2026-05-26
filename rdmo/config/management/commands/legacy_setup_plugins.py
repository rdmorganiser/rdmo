from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from rdmo.config.legacy import get_plugins_from_legacy_settings
from rdmo.config.models import Plugin
from rdmo.config.serializers.v1 import PluginSerializer
from rdmo.core.utils import get_languages


class Command(BaseCommand):
    help = _("Create missing Plugin objects from legacy plugin settings.")

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help=_("Do not write to the database, only print intended actions."),
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        plugins = get_plugins_from_legacy_settings()

        if not plugins:
            self.stdout.write("Nothing to do.")
            return

        self.stdout.write(
            self.style.WARNING(
                "Reading legacy plugin settings. These are deprecated and will be removed in a future release."
            )
        )
        self.save_plugins(plugins, dry_run)

        if dry_run:
            self.stdout.write(self.style.SUCCESS("✔ dry-run complete; no changes committed."))

    def save_plugins(self, plugins, dry_run):
        for plugin_config in sorted(plugins, key=lambda plugin: (plugin["python_path"], plugin["uri_path"])):
            self.save_plugin(plugin_config, dry_run)

    def save_plugin(self, plugin_config, dry_run):
        import_string(plugin_config["python_path"])
        data = self.get_serializer_data(plugin_config)
        existing_plugin = Plugin.objects.filter(python_path=plugin_config["python_path"]).first()
        if not existing_plugin:
            existing_plugin = Plugin.objects.filter(
                uri_prefix=data["uri_prefix"], uri_path=data["uri_path"]
            ).first()

        if existing_plugin:
            self.stdout.write(
                self.style.WARNING(f"skipped(exists): {existing_plugin.python_path} -> {existing_plugin.uri}")
            )
            return

        serializer = PluginSerializer(data=data)
        settings.PLUGINS.append(plugin_config["python_path"])
        serializer.fields["python_path"].choices = [(path, path) for path in settings.PLUGINS]

        try:
            serializer.is_valid(raise_exception=True)
        except RestFrameworkValidationError as e:
            raise CommandError(self.get_validation_error_message(e)) from e
        finally:
            settings.PLUGINS.remove(plugin_config["python_path"])

        if dry_run:
            uri = Plugin.build_uri(data["uri_prefix"], data["uri_path"])
            self.stdout.write(
                self.style.SUCCESS(f"created (dry-run): {plugin_config['python_path']} -> {uri}")
            )
            return

        plugin = serializer.save()
        self.set_multisite(plugin)
        self.stdout.write(
            self.style.SUCCESS(f"created: {plugin.python_path} -> {plugin.uri}")
        )

    def get_serializer_data(self, plugin_config):
        data = {
            "uri_prefix": plugin_config["uri_prefix"] or settings.DEFAULT_URI_PREFIX,
            "uri_path": plugin_config["uri_path"] or plugin_config["url_name"],
            "python_path": plugin_config["python_path"],
            "available": True,
        }

        if plugin_config["url_name"]:
            data["url_name"] = plugin_config["url_name"]

        if plugin_config["title"]:
            data[f"title_{get_languages()[0][0]}"] = plugin_config["title"]

        return data

    def get_validation_error_message(self, error):
        messages = []
        for field, errors in error.detail.items():
            for message in errors:
                messages.append(f"{field}: {message}")
        return "Validation failed: " + "; ".join(messages)

    def set_multisite(self, plugin):
        if settings.MULTISITE:
            current_site = Site.objects.get_current()
            plugin.editors.set([current_site])
            plugin.sites.set([current_site])
