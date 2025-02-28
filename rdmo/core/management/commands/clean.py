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
            self.remove_path('dist')
            self.remove_path('rdmo.egg-info')
        if options['command'] in ['all', 'media']:
            self.remove_path(settings.MEDIA_ROOT)
        if options['command'] in ['all', 'npm']:
            self.remove_path('node_modules')
        if options['command'] in ['all', 'static']:
            self.clean_static()
        if options['command'] in ['all', 'python']:
            self.clean_python()

    def clean_python(self):
        for root, dirs, files in os.walk('.'):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    self.remove_path(os.path.join(root, dir_name), quiet=True)

    def clean_static(self):
        self.remove_path(settings.STATIC_ROOT)

        # hint: `git clean -dfXn` can be used to show all git-ignored files
        for path in [
            'rdmo/core/static/core/css/base.css',
            'rdmo/core/static/core/fonts/',
            'rdmo/core/static/core/js/base.js',
            'rdmo/core/static/core/js/base.js.LICENSE.txt',
            'rdmo/management/static/',
            'rdmo/projects/static/projects/css/interview.css',
            'rdmo/projects/static/projects/css/projects.css',
            'rdmo/projects/static/projects/js/',
        ]:
            self.remove_path(path)

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



