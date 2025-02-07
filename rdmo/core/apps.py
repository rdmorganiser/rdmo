from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'rdmo.core'
    verbose_name = _('Core')

    def ready(self):
        pass
