from django.apps import AppConfig, apps
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = 'rdmo.core'
    verbose_name = _('Core')

    def ready(self):
        if apps.is_installed('drf_spectacular'):
            from . import schema  # noqa: F401
