from lxml import objectify

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from apps.conditions.utils import import_xml as import_conditions
from apps.options.utils import import_xml as import_options
from apps.domain.utils import import_xml as import_domain
from apps.questions.utils import import_xml as import_questions
from apps.views.utils import import_xml as import_views
from apps.projects.utils import import_xml as import_projects


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', action='store', default=False, help='RDMO XML export file')
        parser.add_argument('--user', action='store', default=False, help='RDMO username for this import')

    def handle(self, *args, **options):
        with open(options['xmlfile']) as f:
            xml_root = objectify.parse(f).getroot()

            if xml_root.tag == 'conditions':
                import_conditions(xml_root)

            elif xml_root.tag == 'options':
                import_options(xml_root)

            elif xml_root.tag == 'domain':
                import_domain(xml_root)

            elif xml_root.tag == 'catalogs':
                import_questions(xml_root)

            elif xml_root.tag == 'views':
                import_views(xml_root)

            elif xml_root.tag == 'projects':

                try:
                    user = User.objects.get(username=options['user'])
                except User.DoesNotExist:
                    raise CommandError('Give a valid username using --user.')

                import_projects(xml_root, user)

            else:
                raise Exception('This is not a proper RDMO XML Export.')
