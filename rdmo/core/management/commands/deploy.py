import subprocess

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        print('>>> python manage.py collectstatic --noinput --clear')
        print()
        call_command('collectstatic', '--noinput', '--clear')
        print()

        print('>>> touch config/wsgi.py')
        print()
        subprocess.call(['touch', 'config/wsgi.py'])
        print()
