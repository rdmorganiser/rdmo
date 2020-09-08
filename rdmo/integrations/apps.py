from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class IntegrationsConfig(AppConfig):
    name = 'rdmo.integrations'
    verbose_name = _('Integrations')
