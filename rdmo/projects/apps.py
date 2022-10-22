from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = 'rdmo.projects'
    verbose_name = _('Projects')

    def ready(self):
        from . import rules

        if settings.PROJECT_REMOVE_VIEWS:
            from . import handlers
