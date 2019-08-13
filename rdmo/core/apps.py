import importlib

from django.conf import settings
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    name = 'rdmo.core'
    verbose_name = _('Core')

    def ready(self):
        # import plugins
        for plugin_string in settings.PLUGINS:
            importlib.import_module(plugin_string)
