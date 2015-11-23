import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--html', action='store_true', default=False, help='Create HTML coverage report')

    def handle(self, *args, **options):
        subprocess.call(['coverage', 'run', 'manage.py', 'test'])
        subprocess.call(['coverage', 'report'])
        if options['html']:
            subprocess.call(['coverage', 'html'])
