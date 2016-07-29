from django.core.management.base import BaseCommand

from apps.accounts.testing.factories import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        AdminFactory()
        ManagerFactory()
        UserFactory()
