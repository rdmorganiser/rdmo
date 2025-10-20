from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string

from rdmo.config.models import Plugin


class Command(BaseCommand):
    help = "Check that all configured plugins can be imported"

    def handle(self, *args, **options):
        for plugin in Plugin.objects.all():
            try:
                import_string(plugin.python_path)
                self.stdout.write(self.style.SUCCESS(f"✔ {plugin.python_path}, type={plugin.plugin_type}. OK"))
            except Exception as e:
                if plugin.available:
                    self.stdout.write(self.style.ERROR(
                        f"✖ {plugin.python_path}, type={plugin.plugin_type} failed: {e}")
                    )
                else:
                    self.stdout.write(self.style.WARNING(
                        f"!! {plugin.python_path}, type={plugin.plugin_type} (=unavailable) failed: {e}")
                    )
