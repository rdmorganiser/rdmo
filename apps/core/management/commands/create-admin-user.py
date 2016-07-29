from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
