from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rdmo.projects.handlers.sync_utils import sync_project_instances
from rdmo.projects.models import Project
from rdmo.tasks.models import Task
from rdmo.views.models import View


@receiver(pre_save, sender=Project)
def pre_save_check_if_catalog_was_changed(sender, instance, raw, update_fields, **kwargs):
    instance._catalog_was_changed = False

    if raw or (update_fields and 'catalog' not in update_fields):
        return

    if instance.id is not None:
        # Fetch the original catalog from the database
        if sender.objects.get(id=instance.id).catalog == instance.catalog:
            # Do nothing if the catalog has not changed
            return

    # Defer synchronization of to post_save
    instance._catalog_was_changed = True


@receiver(post_save, sender=Project)
def post_save_project_sync_tasks_when_catalog_was_changed(sender, instance, created, raw, update_fields, **kwargs):
    if raw or (update_fields and 'catalog' not in update_fields):
        return

    if instance._catalog_was_changed or created:
        sync_project_instances(instance, Task)


@receiver(post_save, sender=Project)
def post_save_project_sync_views_when_catalog_was_changed(sender, instance, created, raw, update_fields, **kwargs):
    if raw or (update_fields and 'catalog' not in update_fields):
        return

    if instance._catalog_was_changed or created:
        sync_project_instances(instance, View)
