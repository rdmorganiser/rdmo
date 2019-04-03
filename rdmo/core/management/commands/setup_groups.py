from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from rdmo.accounts.settings import GROUPS
from rdmo.accounts.utils import set_group_permissions

class Command(BaseCommand):

    def handle(self, *args, **options):

        for name, permissions in GROUPS:
            group, created = Group.objects.get_or_create(name=name)

            if created:
                print ('Group "%s" created' % name)
            else:
                group.permissions.clear()

        set_group_permissions()
