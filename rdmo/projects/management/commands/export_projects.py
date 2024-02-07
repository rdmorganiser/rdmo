import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Prefetch

from rdmo.core.plugins import get_plugin
from rdmo.core.utils import render_to_format
from rdmo.projects.models import Project
from rdmo.projects.utils import get_value_path
from rdmo.questions.models import Question, QuestionSet
from rdmo.views.models import View
from rdmo.views.utils import ProjectWrapper

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--answers', action='store_true', help='Export the answers instead of a project')
        parser.add_argument('--view', help='Export a specific view instead of a project')
        parser.add_argument('--format', default='xml', help='Format for the export [default: xml]')
        parser.add_argument('--path', default='exports', help='Directory for the exported files [default: exports]')

    def handle(self, *args, **options):
        self.format = options['format']
        self.path = Path(options['path'])

        if options['answers']:
            self.export_answers()
        elif options['view']:
            self.export_view(options['view'])
        else:
            self.export_projects()

    def get_queryset(self):
        return Project.objects.prefetch_related(
            Prefetch('catalog__sections__questionsets',
                     queryset=QuestionSet.objects.select_related('attribute')),
            Prefetch('catalog__sections__questionsets__questions',
                     queryset=Question.objects.select_related('attribute')),
            Prefetch('catalog__sections__questionsets__questionsets',
                     queryset=QuestionSet.objects.select_related('attribute')),
            Prefetch('catalog__sections__questionsets__questionsets__questions',
                     queryset=Question.objects.select_related('attribute')),
        )

    def export_answers(self):
        current_snapshot = None

        if self.format not in dict(settings.EXPORT_FORMATS):
            raise CommandError(f'Format "{self.format}" is not supported for answers.')

        for project in self.get_queryset():
            context = {
                'project': project,
                'current_snapshot': current_snapshot,
                'project_wrapper': ProjectWrapper(project, current_snapshot),
                'title': project.title,
                'format': self.format,
                'resource_path': get_value_path(project, current_snapshot)
            }

            response = render_to_format(None, context['format'], context['title'],
                                        'projects/project_answers_export.html', context)
            self.write_file(self.path / str(project.id) / 'answers', response)

    def export_view(self, key):
        current_snapshot = None

        if self.format not in dict(settings.EXPORT_FORMATS):
            raise CommandError(f'Format "{self.format}" is not supported for answers.')

        try:
            view = View.objects.get(key=key)
        except View.DoesNotExist as e:
            raise CommandError(f'A view with the key "{key}" was not found.') from e

        for project in self.get_queryset():
            context = {
                'project': project,
                'current_snapshot': current_snapshot,
                'view': project.views.get(pk=view.id),
                'rendered_view': view.render(project, snapshot=current_snapshot, export_format=self.format),
                'project_wrapper': ProjectWrapper(project, current_snapshot),
                'title': project.title,
                'format': self.format,
                'resource_path': get_value_path(project, current_snapshot)
            }

            response = render_to_format(None, context['format'], context['title'],
                                        'projects/project_view_export.html', context)
            self.write_file(self.path / str(project.id) / key, response)

    def export_projects(self):
        for project in self.get_queryset():
            export_plugin = get_plugin('PROJECT_EXPORTS', self.format)
            if export_plugin is None:
                raise CommandError(f'Format "{self.format}" is not supported.')

            export_plugin.project = project
            export_plugin.snapshot = None
            response = export_plugin.render()

            self.write_file(self.path / str(project.id), response)

    def write_file(self, path, response):
        file_name = response.headers['Content-Disposition'].replace('filename=', '').replace('"', '')
        file_path = path / file_name
        file_path.parent.mkdir(exist_ok=True, parents=True)

        print(f'Writing {file_path}')

        with file_path.open('wb') as fp:
            fp.write(response.content)
