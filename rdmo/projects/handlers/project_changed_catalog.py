from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..models import Project
from ..sync import sync_tasks_or_views_for_project


@receiver(pre_save, sender=Project)
def pre_save_check_if_catalog_was_changed(sender, instance, raw, update_fields, **kwargs):
    if (settings.PROJECT_TASKS_SYNC or settings.PROJECT_VIEWS_SYNC) and not raw:
        instance._catalog_was_changed = False

        if instance.id is not None and 'catalog' in update_fields:
            # Fetch the original catalog from the database
            if sender.objects.get(id=instance.id).catalog == instance.catalog:
                # Do nothing if the catalog has not changed
                return
            else:
                # Defer synchronization of to post_save
                instance._catalog_was_changed = True


@receiver(post_save, sender=Project)
def post_save_project_sync_tasks_when_catalog_was_changed(sender, instance, created, raw, update_fields, **kwargs):
    if settings.PROJECT_TASKS_SYNC and not raw and (instance._catalog_was_changed or created):
        sync_tasks_or_views_for_project(Task, instance)


@receiver(post_save, sender=Project)
def post_save_project_sync_views_when_catalog_was_changed(sender, instance, created, raw, update_fields, **kwargs):
    if settings.PROJECT_VIEWS_SYNC and not raw and (instance._catalog_was_changed or created):
        sync_tasks_or_views_for_project(View, instance)
