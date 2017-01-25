from django.core.management.base import BaseCommand

from apps.core.utils import import_xml


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', action='store', default=False, help='RDMO XML export file')

    def handle(self, *args, **options):
        print options['xmlfile']

        with open(options['xmlfile']) as f:
            xml_string = f.read()
            import_xml(xml_string)
