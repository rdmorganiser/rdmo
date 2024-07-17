from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from rdmo.accounts.settings import GROUPS
from rdmo.accounts.utils import set_group_permissions


class Command(BaseCommand):

    def handle(self, *args, **options):

        for name, permissions in GROUPS:
            group, created = Group.objects.get_or_create(name=name)

            if created:
                print(f'Group "{name}" created')
            else:
                group.permissions.clear()

        set_group_permissions()
