import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('command', choices=['make', 'compile'])
        parser.add_argument('-l', '--locale')

    def handle(self, *args, **options):
        if options['command'] == 'make':
            self.handle_make(self, *args, **options)
        elif options['command'] == 'compile':
            self.handle_compile(self, *args, **options)

    def handle_make(self, *args, **options):
        call_args = ['django-admin', 'makemessages']

        if options['locale'] is None:
            call_args.append('--all')
        else:
            call_args.append('-l {locale}'.format(**options))

        subprocess.check_call(call_args, cwd='rdmo')
        subprocess.check_call([*call_args, '-d', 'djangojs'], cwd='rdmo')

    def handle_compile(self, *args, **options):
        call_args = ['django-admin', 'compilemessages']

        if options['locale'] is not None:
            call_args.append('-l {locale}'.format(**options))

        subprocess.check_call(call_args, cwd='rdmo')
