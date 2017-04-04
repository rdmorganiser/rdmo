import subprocess

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        call_command('makemessages', '-l', 'de', ignore=['env', 'env2', 'env3', 'htmlcov'])
        try:
            subprocess.call(['poedit', 'locale/de/LC_MESSAGES/django.po'])
            call_command('compilemessages', '-l', 'de')
        except OSError:
            pass
