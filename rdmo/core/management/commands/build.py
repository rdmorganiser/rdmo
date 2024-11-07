import subprocess
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        subprocess.call(['/bin/bash', '-c', f'{sys.executable} -m build'])
