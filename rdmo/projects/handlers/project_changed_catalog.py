from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..models import Project
from ..sync import sync_tasks_or_views_for_project


@receiver(pre_delete, sender=Catalog)
def clear_progress_for_deleted_catalog(sender, instance, **kwargs):
    # Find affected projects before SET_NULL clears their catalog IDs without calling Project.save().
    Project.objects.filter(catalog_id=instance.id).update(progress_count=None, progress_total=None)


@receiver(post_save, sender=Project)
def post_save_project_sync_tasks_when_catalog_was_changed(sender, instance, created, raw, **kwargs):
    if settings.PROJECT_TASKS_SYNC and not raw and (created or instance._catalog_changed):
        sync_tasks_or_views_for_project(Task, instance)


@receiver(post_save, sender=Project)
def post_save_project_sync_views_when_catalog_was_changed(sender, instance, created, raw, **kwargs):
    if settings.PROJECT_VIEWS_SYNC and not raw and (created or instance._catalog_changed):
        sync_tasks_or_views_for_project(View, instance)
