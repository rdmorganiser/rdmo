from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ConfigConfig(AppConfig):
    name = 'rdmo.config'
    verbose_name = _('Config')
