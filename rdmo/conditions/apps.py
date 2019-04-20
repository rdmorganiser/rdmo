from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConditionsConfig(AppConfig):
    name = 'rdmo.conditions'
    verbose_name = _('Conditions')
