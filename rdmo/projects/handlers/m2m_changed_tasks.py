from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from rdmo.tasks.models import Task

from .generic_handlers import (
    m2m_catalogs_changed_projects_sync_signal_handler,
    m2m_groups_changed_projects_sync_signal_handler,
    m2m_sites_changed_projects_sync_signal_handler,
)


@receiver(m2m_changed, sender=Task.catalogs.through)
def m2m_changed_task_catalog_signal(sender, instance, action, pk_set, **kwargs):
    m2m_catalogs_changed_projects_sync_signal_handler(instance, action, pk_set, 'tasks')


@receiver(m2m_changed, sender=Task.sites.through)
def m2m_changed_task_sites_signal(sender, instance, action, pk_set, **kwargs):
    m2m_sites_changed_projects_sync_signal_handler(instance, action, pk_set, 'tasks')


@receiver(m2m_changed, sender=Task.groups.through)
def m2m_changed_task_groups_signal(sender, instance, action, pk_set, **kwargs):
    m2m_groups_changed_projects_sync_signal_handler(instance, action, pk_set, 'tasks')
