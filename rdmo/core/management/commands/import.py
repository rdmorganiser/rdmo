from lxml import objectify

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from rdmo.conditions.utils import import_conditions
from rdmo.options.utils import import_options
from rdmo.domain.utils import import_domain
from rdmo.questions.utils import import_catalog
from rdmo.tasks.utils import import_tasks
from rdmo.views.utils import import_views
from rdmo.projects.utils import import_projects


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

            elif xml_root.tag == 'catalog':
                import_catalog(xml_root)

            elif xml_root.tag == 'tasks':
                import_tasks(xml_root)

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
