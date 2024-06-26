import logging

from django.core.management.base import BaseCommand, CommandError

from rdmo.core.xml import parse_xml_to_elements
from rdmo.management.imports import import_elements

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', action='store', default=False, help='RDMO XML export file')

    def handle(self, *args, **options):

        try:
            xml_parsed_elements, errors = parse_xml_to_elements(xml_file=options['xmlfile'])
        except CommandError as e:
            logger.info('Import failed with XML parsing errors.')
            raise CommandError(str(e)) from e

        # raise exception when xml parsing returned any errors
        if errors:
            logger.info('Import failed with XML validation errors.')
            raise CommandError(" ".join(map(str, errors)))

        import_elements(xml_parsed_elements)
