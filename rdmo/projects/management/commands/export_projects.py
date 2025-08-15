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
            '--export-mode',
            choices=['project', 'answers', 'view'],
            default='project',
            help='What to export: project (default), answers or view.'
        )
        parser.add_argument(
            '--view-uri',
            metavar='URI',
            help='Required if export-mode is "view". Specifies the view URI to export.'
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
            '--path', default='exports', metavar='DIR', help='Target directory (default: exports/).'
        )
        parser.add_argument(
            '--include-memberships', action='store_true',
            help='Write project memberships (role, user, email) to export.'
        )

    def handle(self, *args, **options):
        export_mode = options['export_mode']
        export_format: str = options['format']
        export_path: Path = Path(options['path']).expanduser().resolve()
        include_memberships: bool = options['include_memberships']
        project_ids = options.get('projects') or None
        site_id: int = options['site_id']
        catalog_uri = options.get('catalog_uri') or None
        # validations first
        if export_mode in ('answers', 'view'):
            if export_format not in dict((*settings.EXPORT_FORMATS, ('xml', None))):
                raise CommandError(
                    f'Format "{export_format}" is not configured in settings.EXPORT_FORMATS for export mode {export_mode}.'  # noqa: E501
                )

        if export_mode == 'view':
            if not options.get('view_uri'):
                raise CommandError('You must specify --view-uri when using export-mode="view".')

        if include_memberships and export_mode != 'project':
            raise CommandError("Project memberships can only be exported with export mode 'project'.")

        if site_id != settings.SITE_ID and not Site.objects.filter(id=site_id).exists():
            raise CommandError(f'No matching site for id={site_id} found.')

        # start: query the projects
        projects = self.get_project_queryset(project_ids, site_id, catalog_uri)
        if include_memberships:
            projects = self.prefetch_memberships(projects)

        if not projects.exists():
            self.stdout.write(self.style.WARNING('No projects found.'))
            if catalog_uri:
                raise CommandError(f'No matching projects found for catalog(uri={catalog_uri}).')

        # loop through projects
        for project in projects:
            # export individual project based on format,mode,path and kwargs
            self.export_project(
                project, export_format, export_mode, export_path,
                view_uri=options['view_uri'],
                include_memberships=include_memberships
            )

        self.stdout.write(self.style.SUCCESS(f'Exported {projects.count()} project(s) to {export_path}'))

    def export_project(self, project, export_format, export_mode, export_path,
                       view_uri=None, include_memberships=False
        ) -> None:
        if export_mode == 'answers':
            response = self.render_answers(project, export_format)
            subdir = 'answers'

        elif export_mode == 'view':
            try:
                view = View.objects.get(uri=view_uri)
            except View.DoesNotExist as exc:
                raise CommandError(f'View with uri "{view_uri}" does not exist.') from exc

            response = self.render_view(project, export_format, view=view)
            subdir = 'views/' + view.uri_path

        else:  # full project
            response = self.render_full_project(project, export_format, include_memberships=include_memberships)
            subdir = ''

        if response.status_code != 200:
            raise CommandError(f"Failed to export project '{project.title}'\nResponse={response}\n\t{response.content.decode()}."  # noqa: E501
            )

        target_dir = export_path / str(project.id) / subdir
        target_filename = self.get_filename_from_response(response)
        target_file = target_dir / target_filename

        self.write_content_to_file(target_file, response.content)
        self.stdout.write(self.style.SUCCESS(f'Exported {project} to {target_file}'))

    @staticmethod
    def get_project_queryset(ids, site_id, catalog_uri, ) -> QuerySet[Project]:

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
    def prefetch_memberships(qs):
        return  qs.prefetch_related(
            Prefetch(
                'memberships',
                queryset=Membership.objects.select_related('user'),
            )
        )

    @staticmethod
    def render_answers(project, export_format):
        snapshot = None
        context = {
            'project': project,
            'current_snapshot': snapshot,
            'project_wrapper': ProjectWrapper(project, snapshot),
            'title': project.title,
            'format': export_format,
            'resource_path': get_value_path(project, snapshot),
        }
        return render_to_format(
            None, export_format,
            context['title'], 'projects/project_answers_export.html', context
        )

    @staticmethod
    def render_view(project, export_format, view):
        snapshot = None
        context = {
            'project': project,
            'current_snapshot': snapshot,
            'view': view,
            'rendered_view': view.render(project, snapshot=snapshot, export_format=export_format),
            'project_wrapper': ProjectWrapper(project, snapshot),
            'title': project.title,
            'format': export_format,
            'resource_path': get_value_path(project, snapshot),
        }
        return render_to_format(
            None, export_format, context['title'], 'projects/project_view_export.html', context
        )

    @staticmethod
    def render_full_project(project, export_format, include_memberships: bool=False) -> dict:
        plugin_cls = get_plugin('PROJECT_EXPORTS', export_format)
        if plugin_cls is None:
            raise CommandError(f'Format "{export_format}" is not supported.')
        plugin = plugin_cls
        plugin.project = project
        plugin.snapshot = None
        plugin.include_memberships = include_memberships
        return plugin.render()

    @staticmethod
    def get_filename_from_response(response):
        filename = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
        if not filename:
            raise CommandError('Export response did not include a filename header.')
        return filename

    @staticmethod
    def write_content_to_file(target_file: Path, content) -> None:

        if not target_file.parent.exists():
            target_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            logger.info('Writing %s', target_file)
            with target_file.open('wb') as fp:
                fp.write(content)
        except FileNotFoundError as e:
            raise CommandError(f'Failed to write to {target_file}: file not found.') from e
        except OSError as e:
            # Handle broader I/O errors like permission denied, disk full, etc.
            raise CommandError(f'Failed to write to {target_file}: {e}') from e
