from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rdmo.projects.models import Project
from rdmo.tasks.models import Task

DEFERRED_SYNC_TASKS_KEY = '_deferred_sync_tasks'

@receiver(pre_save, sender=Project)
def pre_save_project_sync_tasks_from_catalog(sender, instance, raw, update_fields, **kwargs):
    if (raw or
        instance.id is None or
        (update_fields and 'catalog' not in update_fields)
    ):
        return

    # Fetch the original catalog from the database
    original_instance = sender.objects.get(id=instance.id)
    if original_instance.catalog == instance.catalog:
        # Do nothing if the catalog has not changed
        return

    # Defer synchronization of views
    setattr(instance, DEFERRED_SYNC_TASKS_KEY, True)

@receiver(post_save, sender=Project)
def post_save_project_sync_tasks_from_catalog(sender, instance, created, raw, **kwargs):
    if not hasattr(instance, DEFERRED_SYNC_TASKS_KEY):
        return
    if getattr(instance, DEFERRED_SYNC_TASKS_KEY, None) or (created and not raw):
        # For existing projects with catalog changes, use deferred views
        instance.views.set(Task.objects.filter_available_tasks_for_project(instance))
        delattr(instance, DEFERRED_SYNC_TASKS_KEY)
