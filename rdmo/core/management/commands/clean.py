import os
import shutil
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', choices=[
            'all',
            'dist',
            'media',
            'npm',
            'python',
            'static',
        ])

    def handle(self, *args, **options):
        if options['command'] in ['all', 'dist']:
            self.remove_path('dist')
            self.remove_path('rdmo.egg-info')
        if options['command'] in ['all', 'static']:
            self.remove_path(settings.STATIC_ROOT)
        if options['command'] in ['all', 'media']:
            self.remove_path(settings.MEDIA_ROOT)
        if options['command'] in ['all', 'npm']:
            self.remove_path('node_modules')
        if options['command'] in ['all', 'python']:
            self.clean_python()
        if options['command'] in ['all', 'git']:
            subprocess.call(['git', 'clean', '-fd'])

    def clean_python(self):
        for root, dirs, _ in os.walk('.'):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    self.remove_path(os.path.join(root, dir_name), quiet=True)

    def remove_path(self, path, quiet=False):
        if path and os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
                if not quiet:
                    print(f'Directory "{path}" has been removed!')
            elif os.path.isfile(path):
                os.remove(path)
                if not quiet:
                    print(f'File "{path}" has been removed!')
