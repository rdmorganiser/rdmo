from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rdmo.projects.models import Project
from rdmo.views.models import View

DEFERRED_SYNC_VIEWS_KEY = '_deferred_sync_views'

@receiver(pre_save, sender=Project)
def pre_save_project_sync_views_from_catalog(sender, instance, raw, update_fields, **kwargs):
    if raw or (update_fields and 'catalog' not in update_fields):
        return

    # Fetch the original catalog from the database
    original_instance = sender.objects.get(id=instance.id)
    if original_instance.catalog == instance.catalog:
        # Do nothing if the catalog has not changed
        return

    # Defer synchronization of views
    setattr(instance, DEFERRED_SYNC_VIEWS_KEY, True)

@receiver(post_save, sender=Project)
def post_save_project_sync_views_from_catalog(sender, instance, created, raw, update_fields, **kwargs):
    if getattr(instance, DEFERRED_SYNC_VIEWS_KEY, None) or (created and not raw):
        # For existing projects with catalog changes, use deferred views
        instance.views.set(View.objects.filter_available_views_for_project(instance))
        delattr(instance, DEFERRED_SYNC_VIEWS_KEY)
