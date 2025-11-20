import subprocess
import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            import build  # noqa: F401
        except ImportError as e:
            raise CommandError('build is not installed.') from e

        call_command('npm', 'ci')
        call_command('npm', 'run', 'build:prod')
        subprocess.call(['/bin/bash', '-c', f'{sys.executable} -m build'])
