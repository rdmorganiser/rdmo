import logging
import xml.etree.ElementTree as et

from django.core.management.base import BaseCommand

from rdmo.conditions.imports import import_conditions
from rdmo.domain.imports import import_domain
from rdmo.options.imports import import_options
# from rdmo.projects.imports import import_project
from rdmo.questions.imports import import_questions
from rdmo.tasks.imports import import_tasks
from rdmo.views.imports import import_views

log = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('xmlfile', action='store', default=False, help='RDMO XML export file')
        parser.add_argument('--user', action='store', default=False, help='RDMO username for this import')

    def handle(self, *args, **options):

        tree = et.parse(options['xmlfile'])
        root = tree.getroot()

        if root.tag == 'rdmo':
            import_conditions(root)
            import_options(root)
            import_domain(root)
            import_questions(root)
            import_tasks(root)
            import_views(root)
