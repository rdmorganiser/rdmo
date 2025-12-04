import os
import shutil
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', choices=[
            'all',
            'build',
            'git',
            'media',
            'npm',
            'static',
        ])

    def handle(self, *args, **options):
        if options['command'] in ['all', 'build']:
            self.remove_path('dist')
            self.remove_path('rdmo.egg-info')

        if options['command'] in ['all', 'git']:
            subprocess.call(['git', 'clean', '-dfx'], cwd='rdmo')

        if options['command'] in ['all', 'media']:
            self.remove_path(settings.MEDIA_ROOT)

        if options['command'] in ['all', 'npm']:
            self.remove_path('node_modules')

        if options['command'] in ['all', 'static']:
            self.remove_path(settings.STATIC_ROOT)

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
