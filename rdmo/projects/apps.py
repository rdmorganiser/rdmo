from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = 'rdmo.projects'
    verbose_name = _('Projects')

    def ready(self):
        from . import rules  # noqa: F401

        if settings.PROJECT_VIEWS_SYNC:
            from .handlers import project_views  # noqa: F401
        if settings.PROJECT_TASKS_SYNC:
            from .handlers import project_tasks  # noqa: F401
