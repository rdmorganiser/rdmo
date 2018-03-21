import io
import logging

# from lxml import objectify

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from rdmo.core.imports import validate_xml
from rdmo.conditions.imports import import_conditions
from rdmo.options.imports import import_options
from rdmo.domain.imports import import_domain
# from rdmo.questions.utils import import_catalog
from rdmo.tasks.imports import import_tasks
from rdmo.views.imports import import_views
from rdmo.projects.imports import import_project

log = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', action='store', default=False, help='RDMO XML export file')
        parser.add_argument('--user', action='store', default=False, help='RDMO username for this import')

    def handle(self, *args, **options):
        with io.open(options['xmlfile'], encoding='utf8') as f:

            roottag, xmltree = validate_xml(f)

            if roottag == 'conditions':
                print('Importing conditions...')
                import_conditions(xmltree)
                print('Done.\n')

            elif roottag == 'options':
                print('Importing options...')
                import_options(xmltree)
                print('Done.\n')

            elif roottag == 'domain':
                print('Importing domain...')
                import_domain(xmltree)
                print('Done.\n')

            elif roottag == 'tasks':
                print('Importing tasks...')
                import_tasks(xmltree)
                print('Done.\n')

            elif roottag == 'views':
                print('Importing views...')
                import_views(xmltree)
                print('Done.\n')

            elif roottag == 'project':
                print('Importing project...')
                try:
                    user = User.objects.get(username=options['user'])
                except User.DoesNotExist:
                    raise CommandError('Give a valid username using --user.')
                import_project(xmltree, user)
                print('Done.\n')

            # obsolete, to be removed later
            # xml_root = objectify.parse(f).getroot()
            # if xml_root.tag == 'catalog':
            #     import_catalog(xml_root)
