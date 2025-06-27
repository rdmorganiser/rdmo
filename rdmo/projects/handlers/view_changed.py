from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from rdmo.views.models import View

from .sync_utils import sync_task_or_view_to_projects


@receiver(post_save, sender=View)
def view_changed_availability_handler(sender, instance, created, raw, update_fields, **kwargs):
    if raw or (update_fields and 'available' not in update_fields):
        return
    sync_task_or_view_to_projects(instance)


@receiver(m2m_changed, sender=View.catalogs.through)
def m2m_changed_view_catalog_signal(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_task_or_view_to_projects(instance)


@receiver(m2m_changed, sender=View.sites.through)
def m2m_changed_view_sites_signal(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_task_or_view_to_projects(instance)


@receiver(m2m_changed, sender=View.groups.through)
def m2m_changed_view_groups_signal(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        sync_task_or_view_to_projects(instance)
