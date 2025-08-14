from __future__ import annotations

import logging
from pathlib import Path

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Prefetch, QuerySet

from rdmo.core.plugins import get_plugin
from rdmo.core.utils import render_to_format
from rdmo.projects.models import Membership, Project
from rdmo.projects.utils import get_value_path
from rdmo.views.models import View
from rdmo.views.utils import ProjectWrapper

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--answers', action='store_true', help='Export answers instead of the full project.'
        )
        parser.add_argument(
            '--view', metavar='URI', help='Export the given view instead of the full project.'
        )
        parser.add_argument(
            '--projects', nargs='*', type=int, metavar='ID', help='Limit the export to specific project IDs.'
        )
        parser.add_argument(
            '--site-id',
            type=int,
            default=settings.SITE_ID,
            help='Filter projects by site ID (default: settings.SITE_ID).',
        )
        parser.add_argument('--catalog-uri', metavar='URI', help='Filter projects by the catalog URI.')
        parser.add_argument(
            '--format', default='xml', help='Export format (answers/view honour settings.EXPORT_FORMATS).'
        )
        parser.add_argument(
            '--path', default='exports', metavar='DIR', help='Target directory [default: exports/].'
        )
        parser.add_argument(
            '--with-members', action='store_true',
            help='Write project memberships (user, role, email) to export.'
        )

    def handle(self, *args, **options):
        export_mode = 'answers' if options['answers'] else 'view' if options['view'] else 'project'

        self.format: str = options['format']
        self.path: Path = Path(options['path']).expanduser().resolve()
        self.with_members: bool = options['with_members']
        project_ids = options.get('projects') or None
        site_id: int = options['site_id']
        catalog_uri= options.get('catalog_uri') or None
        # validations first
        if export_mode in ('answers', 'view'):
            if self.format not in dict((*settings.EXPORT_FORMATS,('xml',None))):
                raise CommandError(
                    f'Format "{self.format}" is not configured in settings.EXPORT_FORMATS for export mode {export_mode}.'  # noqa: E501
                )
        if export_mode == 'view':
            try:
                view_obj = View.objects.get(uri=options['view'])
            except View.DoesNotExist as exc:
                raise CommandError(f'View with uri "{options["view"]}" does not exist.') from exc
        else:
            view_obj = None

        if site_id != settings.SITE_ID and not Site.objects.filter(id=site_id).exists():
            raise CommandError(f'No matching site for id={site_id} found.')

        projects = self._get_queryset(project_ids, site_id, catalog_uri)
        if self.with_members:
            projects = self._prefetch_memberships(projects)

        if not projects.exists():
            self.stdout.write(self.style.WARNING('No projects found.'))
            if catalog_uri:
                raise CommandError(f'No matching projects found for catalog(uri={catalog_uri}).')

        for project in projects:
            self.export_project(project, mode=export_mode, view=view_obj, include_memberships=self.with_members)

        self.stdout.write(self.style.SUCCESS(f'Exported {projects.count()} project(s) to {self.path}'))

    def _get_queryset(self,ids,site_id,catalog_uri,) -> QuerySet[Project]:

        # start from the selected site
        qs = Project.objects.filter(site_id=site_id)

        # optional catalog URI filter
        if catalog_uri:
            qs = qs.filter(catalog__uri=catalog_uri)

        # explicit project IDs
        if ids:
            qs = qs.filter(id__in=set(ids))

        return qs.select_related('catalog', 'site')

    @staticmethod
    def _prefetch_memberships(qs):
        return  qs.prefetch_related(
            Prefetch(
                'memberships',
                queryset=Membership.objects.select_related('user'),
            )
        )

    def export_project(self, project, *, mode: str, view=None, include_memberships=False) -> None:
        if mode == 'answers':
            response = self.render_answers(project)
            subdir = 'answers'

        elif mode == 'view':
            response = self.render_view(project, view)
            subdir = view.uri_path

        else:  # full project
            response = self.render_full_project(project, include_memberships=include_memberships)
            subdir = ''

        target_dir = self.path / str(project.id) / subdir
        self.write_response_to_file(target_dir, response)

    def render_answers(self, project):
        snapshot = None
        context = {
            'project': project,
            'current_snapshot': snapshot,
            'project_wrapper': ProjectWrapper(project, snapshot),
            'title': project.title,
            'format': self.format,
            'resource_path': get_value_path(project, snapshot),
        }
        return render_to_format(
            None, self.format, context['title'], 'projects/project_answers_export.html', context
        )

    def render_view(self, project, view: View):
        snapshot = None
        context = {
            'project': project,
            'current_snapshot': snapshot,
            'view': project.views.get(pk=view.id),
            'rendered_view': view.render(project, snapshot=snapshot, export_format=self.format),
            'project_wrapper': ProjectWrapper(project, snapshot),
            'title': project.title,
            'format': self.format,
            'resource_path': get_value_path(project, snapshot),
        }
        return render_to_format(
            None, self.format, context['title'], 'projects/project_view_export.html', context
        )

    def render_full_project(self, project, include_memberships: bool=False) -> dict:
        plugin_cls = get_plugin('PROJECT_EXPORTS', self.format)
        if plugin_cls is None:
            raise CommandError(f'Format "{self.format}" is not supported.')
        plugin = plugin_cls
        plugin.project = project
        plugin.snapshot = None
        plugin.include_memberships = include_memberships
        return plugin.render()

    @staticmethod
    def write_response_to_file(target_dir: Path, response,) -> None:
        filename = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
        if not filename:
            raise CommandError('Export response did not include a filename header.')

        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / filename
        logger.info('Writing %s', file_path)
        with file_path.open('wb') as fp:
            fp.write(response.content)
