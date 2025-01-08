
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from rdmo.views.models import View

from .generic_handlers import (
    m2m_catalogs_changed_projects_sync_signal_handler,
    m2m_groups_changed_projects_sync_signal_handler,
    m2m_sites_changed_projects_sync_signal_handler,
)


@receiver(m2m_changed, sender=View.catalogs.through)
def m2m_changed_view_catalog_signal(sender, instance, action, model, pk_set, **kwargs):
    m2m_catalogs_changed_projects_sync_signal_handler(
        action=action,
        related_model=model,
        pk_set=pk_set,
        instance=instance,
        project_field='views',
    )



@receiver(m2m_changed, sender=View.sites.through)
def m2m_changed_view_sites_signal(sender, instance, action, model, pk_set, **kwargs):
    m2m_sites_changed_projects_sync_signal_handler(
        action=action,
        model=model,
        pk_set=pk_set,
        instance=instance,
        project_field='views'
    )


@receiver(m2m_changed, sender=View.groups.through)
def m2m_changed_view_groups_signal(sender, instance, action, model, pk_set, **kwargs):
    m2m_groups_changed_projects_sync_signal_handler(
        action=action,
        model=model,
        pk_set=pk_set,
        instance=instance,
        project_field='views'
    )
