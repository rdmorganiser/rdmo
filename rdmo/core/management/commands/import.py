import io
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from rdmo.core.imports import validate_xml
from rdmo.conditions.imports import import_conditions
from rdmo.domain.imports import import_domain
from rdmo.options.imports import import_options
from rdmo.projects.imports import import_project
from rdmo.questions.imports import import_catalog
from rdmo.tasks.imports import import_tasks
from rdmo.views.imports import import_views

log = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', action='store', default=False, help='RDMO XML export file')
        parser.add_argument('--user', action='store', default=False, help='RDMO username for this import')

    def handle(self, *args, **options):
        with io.open(options['xmlfile'], encoding='utf8') as filedata:

            roottag, xmltree = validate_xml(filedata)

            if roottag == 'conditions':
                import_conditions(xmltree)

            elif roottag == 'options':
                import_options(xmltree)

            elif roottag == 'domain':
                import_domain(xmltree)

            elif roottag == 'catalog':
                import_catalog(xmltree)

            elif roottag == 'tasks':
                import_tasks(xmltree)

            elif roottag == 'views':
                import_views(xmltree)

            elif roottag == 'project':
                try:
                    user = User.objects.get(username=options['user'])
                except User.DoesNotExist:
                    raise CommandError('Give a valid username using --user.')
                import_project(xmltree, user)
