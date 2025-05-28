from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from rdmo.tasks.models import Task

from .projects_sync import sync_instance_to_projects


@receiver(m2m_changed, sender=Task.catalogs.through)
def m2m_changed_task_catalog_signal(sender, instance, action, pk_set, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_instance_to_projects(instance)


@receiver(m2m_changed, sender=Task.sites.through)
def m2m_changed_task_sites_signal(sender, instance, action, pk_set, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_instance_to_projects(instance)


@receiver(m2m_changed, sender=Task.groups.through)
def m2m_changed_task_groups_signal(sender, instance, action, pk_set, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_instance_to_projects(instance)
