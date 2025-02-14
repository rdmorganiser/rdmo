from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from rdmo.projects.models import Project
from rdmo.views.models import View


@receiver(pre_save, sender=Project)
def pre_save_project_sync_views_from_catalog(sender, instance, raw, update_fields, **kwargs):
    instance._catalog_has_changed_sync_views = False

    if raw or (update_fields and 'catalog' not in update_fields):
        return

    if instance.id is not None:
        # Fetch the original catalog from the database
        if sender.objects.get(id=instance.id).catalog == instance.catalog:
            # Do nothing if the catalog has not changed
            return

    # Defer synchronization of views
    instance._catalog_has_changed_sync_views = True


@receiver(post_save, sender=Project)
def post_save_project_sync_views_from_catalog(sender, instance, created, raw, update_fields, **kwargs):
    if raw or (update_fields and 'catalog' not in update_fields):
        return

    if instance._catalog_has_changed_sync_views or (created and not instance.views.exists):
        instance.views.set(View.objects.filter_available_views_for_project(instance).values_list('id', flat=True))
