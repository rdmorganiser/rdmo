from django.db.models.signals import post_save
from django.dispatch import receiver

from rdmo.projects.handlers.sync_utils import sync_tasks_or_views_on_a_project
from rdmo.projects.models import Membership
from rdmo.tasks.models import Task
from rdmo.views.models import View


@receiver(post_save, sender=Membership)
def post_save_membership_sync_tasks(sender, instance, created, raw, update_fields, **kwargs):
    if not raw:
        sync_tasks_or_views_on_a_project(instance.project, Task)


@receiver(post_save, sender=Membership)
def post_save_membership_sync_views(sender, instance, created, raw, update_fields, **kwargs):
    if not raw:
        sync_tasks_or_views_on_a_project(instance.project, View)
