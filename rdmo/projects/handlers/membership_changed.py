from django.db.models.signals import post_save
from django.dispatch import receiver

from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..models import Membership
from ..sync import sync_tasks_or_views_for_project


@receiver(post_save, sender=Membership)
def post_save_membership_sync_tasks(sender, instance, created, raw, update_fields, **kwargs):
    if not raw:
        sync_tasks_or_views_for_project(Task, instance.project)


@receiver(post_save, sender=Membership)
def post_save_membership_sync_views(sender, instance, created, raw, update_fields, **kwargs):
    if not raw:
        sync_tasks_or_views_for_project(View, instance.project)
