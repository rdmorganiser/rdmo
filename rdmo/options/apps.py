from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OptionsConfig(AppConfig):
    name = 'rdmo.options'
    verbose_name = _('Options')
