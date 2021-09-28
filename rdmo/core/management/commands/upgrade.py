import subprocess

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        print()

        print('>>> python manage.py migrate')
        print()
        call_command('migrate')
        print()

        print('>>> python manage.py download_vendor_files')
        print()
        call_command('download_vendor_files')
        print()

        print('>>> python manage.py collectstatic --noinput --clear')
        print()
        call_command('collectstatic', '--noinput', '--clear')
        print()

        print('>>> touch config/wsgi.py')
        print()
        subprocess.call(['touch', 'config/wsgi.py'])
