import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', choices=['make', 'compile'])

    def handle(self, *args, **options):
        if options['command'] == 'make':
            subprocess.check_call(['django-admin', 'makemessages', '--all'], cwd='rdmo')
            subprocess.check_call(['django-admin', 'makemessages', '--all', '-d', 'djangojs'], cwd='rdmo')

        elif options['command'] == 'compile':
            subprocess.check_call(['django-admin', 'compilemessages'], cwd='rdmo')
