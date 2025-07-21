from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = 'rdmo.projects'
    verbose_name = _('Projects')

    def ready(self):
        from . import rules  # noqa: F401

        if settings.PROJECT_VIEWS_SYNC:
            from .handlers import view_changed  # noqa: F401
            from .handlers.project_changed_catalog import (  # noqa: F401
                post_save_project_sync_views_when_catalog_was_changed,
                pre_save_check_if_catalog_was_changed,
            )
        if settings.PROJECT_TASKS_SYNC:
            from .handlers import task_changed  # noqa: F401
            from .handlers.project_changed_catalog import (  # noqa: F401
                post_save_project_sync_tasks_when_catalog_was_changed,
                pre_save_check_if_catalog_was_changed,
            )
