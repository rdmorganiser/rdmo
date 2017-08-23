from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from rdmo.accounts.settings import GROUPS

class Command(BaseCommand):

    def handle(self, *args, **options):

        for name, permissions in GROUPS:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                print ('Group "%s" created' % name)
                for codename in permissions:
                    group.permissions.add(Permission.objects.get(codename=codename))
