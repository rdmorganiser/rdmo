import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('locale')
        parser.add_argument('--js', action='store_true')

    def handle(self, *args, **options):
        locale = options['locale']
        file = 'djangojs' if options['js'] else 'django'
        subprocess.check_call(['poedit', f'rdmo/locale/{locale}/LC_MESSAGES/{file}.po'])
