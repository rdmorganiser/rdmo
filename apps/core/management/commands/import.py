from lxml import objectify

from django.core.management.base import BaseCommand

from apps.conditions.utils import import_xml as import_conditions
from apps.options.utils import import_xml as import_options
#from apps.domain.utils import import_xml as import_domain
#from apps.questions.utils import import_xml as import_questions


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', action='store', default=False, help='RDMO XML export file')

    def handle(self, *args, **options):
        with open(options['xmlfile']) as f:
            xml_string = f.read()
            xml_root = objectify.fromstring(xml_string)

            if xml_root.tag == 'conditions':
                import_conditions(xml_root)

            elif xml_root.tag == 'options':
                import_options(xml_root)

            elif xml_root.tag == 'domain':
                import_domain(xml_root)

            elif xml_root.tag == 'catalogs':
                import_questions(xml_root)

            else:
                raise Exception('This is not a proper RDMO XML Export.')
