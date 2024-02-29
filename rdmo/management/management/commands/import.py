import logging

from django.core.management.base import BaseCommand, CommandError

from rdmo.core.xml import XmlToElementsParser
from rdmo.management.imports import import_elements

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', action='store', default=False, help='RDMO XML export file')

    def handle(self, *args, **options):

        try:
            xml_parser = XmlToElementsParser(file_name=options['xmlfile'])
        except CommandError as e:
            logger.info('Import failed with XML parsing errors.')
            raise CommandError(str(e)) from e

        # step 7: check if valid
        if not xml_parser.is_valid():
            logger.info('Import failed with XML validation errors.')
            raise CommandError(" ".join(map(str, xml_parser.errors)))

        import_elements(xml_parser.parsed_elements)
