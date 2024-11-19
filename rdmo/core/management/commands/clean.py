import os
import shutil

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
            self.clean_dir('dist')
            self.clean_dir('rdmo.egg-info')
        if options['command'] in ['all', 'media']:
            self.clean_dir(settings.MEDIA_ROOT)
        if options['command'] in ['all', 'npm']:
            self.clean_dir('node_modules')
        if options['command'] in ['all', 'static']:
            self.clean_static()
        if options['command'] in ['all', 'python']:
            self.clean_python()

    def clean_python(self):
        for root, dirs, files in os.walk('.'):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    self.clean_dir(os.path.join(root, dir_name), quiet=True)

    def clean_static(self):
        self.clean_dir(settings.STATIC_ROOT)

        for path in [
            # 'rdmo/core/static',     # TODO: enable after cleanup
            'rdmo/management/static',
            # 'rdmo/projects/static'  # TODO: enable after cleanup
        ]:
            self.clean_dir(path)

    def clean_dir(self, path, quiet=False):
        if path and os.path.exists(path):
            shutil.rmtree(path)
            if not quiet:
                print(f'Directory "{path}" has been removed!')
