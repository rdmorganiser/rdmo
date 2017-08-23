from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', action='store', help='Username of the new admin.')

    def handle(self, *args, **options):
        user = User.objects.get(username=options['username'])
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
