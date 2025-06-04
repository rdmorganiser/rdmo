from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from rdmo.tasks.models import Task

from .sync_utils import sync_instance_to_projects


@receiver(post_save, sender=Task)
def task_changed_availability_handler(sender, instance, created, raw, update_fields, **kwargs):
    if raw or (update_fields and 'available' not in update_fields):
        return
    sync_instance_to_projects(instance)

@receiver(m2m_changed, sender=Task.catalogs.through)
def m2m_changed_task_catalog_signal(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_instance_to_projects(instance)


@receiver(m2m_changed, sender=Task.sites.through)
def m2m_changed_task_sites_signal(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_instance_to_projects(instance)


@receiver(m2m_changed, sender=Task.groups.through)
def m2m_changed_task_groups_signal(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_instance_to_projects(instance)
