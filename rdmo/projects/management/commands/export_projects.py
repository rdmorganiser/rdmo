from __future__ import annotations

import json
import logging
from pathlib import Path

from django.conf import settings
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
        parser.add_argument('--answers', action='store_true', help='Export answers instead of the full project.')
        parser.add_argument('--view', metavar='URI', help='Export the given view instead of the full project.')
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
        parser.add_argument('--path', default='exports', metavar='DIR', help='Target directory [default: exports/].')
        parser.add_argument(
            '--with-members', action='store_true', help='Write a members.json file with user/role info.'
        )

    def handle(self, *args, **options):
        export_mode = 'answers' if options['answers'] else 'view' if options['view'] else 'project'

        self.format: str = options['format']
        self.path: Path = Path(options['path']).expanduser().resolve()
        self.with_members: bool = options['with_members']
        project_ids = options.get('projects') or None
        site_id: int = options['site_id']
        catalog_uri= options.get('catalog_uri') or None

        # upfront validations ------------------------------------------------
        if export_mode in ('answers', 'view'):
            if self.format not in dict(settings.EXPORT_FORMATS):
                raise CommandError(f'Format "{self.format}" is not configured in settings.EXPORT_FORMATS.')

        view_obj= None
        if export_mode == 'view':
            try:
                view_obj = View.objects.get(uri=options['view'])
            except View.DoesNotExist as exc:
                raise CommandError(f'View with key "{options["view"]}" does not exist.') from exc

        projects = self._get_queryset(project_ids, site_id, catalog_uri)
        if not projects.exists():
            if catalog_uri:
                project_catalogs = sorted(
                    set(self._get_queryset(project_ids, site_id, None).values_list('catalog__uri', flat=True))
                )
                project_catalogs_str = [f"\t- {i} \n" for i in project_catalogs]
                self.stdout.write(self.style.WARNING(f'Choose a catalog from:\n {"".join(project_catalogs_str)}'))

            if site_id != settings.SITE_ID:
                project_sites = sorted(
                    set(self._get_queryset(project_ids, None, None).values_list('site__id', 'site__domain'))
                )
                project_sites_str = [f"\t- {id} {domain} \n" for id, domain in project_sites]
                self.stdout.write(self.style.WARNING(f'Choose a site from:\n {"".join(project_sites_str)}'))

            raise CommandError('No matching projects found.')

        for project in projects:
            self._export_project(project, mode=export_mode, view=view_obj)

        self.stdout.write(self.style.SUCCESS(f'Exported {projects.count()} project(s) to {self.path}'))

    def _get_queryset(
        self,
        ids,
        site_id,
        catalog_uri,
    ) -> QuerySet[Project]:
        """
        Build a base queryset filtered by site_id and optional catalog_uri,
        then by explicit project IDs if given.
        """
        # start from the current site
        if site_id is not None:
            qs = Project.objects.filter(site_id=site_id)
        else:
            qs = Project.objects.all()

        # optional catalog URI filter
        if catalog_uri:
            qs = qs.filter(catalog__uri=catalog_uri)

        # explicit project IDs
        if ids:
            qs = qs.filter(id__in=set(ids))

        return qs.select_related('catalog', 'site').prefetch_related(
            Prefetch(
                'memberships',
                queryset=Membership.objects.select_related('user'),
            )
        )

    def _export_project(
        self,
        project: Project,
        *,
        mode: str,
        view= None,
    ) -> None:
        """
        Orchestrate the chosen export *mode* for one project and write the file
        to disk.
        """
        if mode == 'answers':
            response = self._render_answers(project)
            subdir = 'answers'

        elif mode == 'view':
            assert view is not None  # guarded in `handle`
            response = self._render_view(project, view)
            subdir = view.uri_path

        else:  # full project
            response = self._render_full_project(project)
            subdir = ''

        self._write_response(project, subdir, response)

        if self.with_members:
            self._write_members_json(project)

    def _render_answers(self, project: Project):
        snapshot = None
        context = {
            'project': project,
            'current_snapshot': snapshot,
            'project_wrapper': ProjectWrapper(project, snapshot),
            'title': project.title,
            'format': self.format,
            'resource_path': get_value_path(project, snapshot),
        }
        return render_to_format(None, self.format, context['title'], 'projects/project_answers_export.html', context)

    def _render_view(self, project: Project, view: View):
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
        return render_to_format(None, self.format, context['title'], 'projects/project_view_export.html', context)

    def _render_full_project(self, project: Project):
        plugin_cls = get_plugin('PROJECT_EXPORTS', self.format)
        if plugin_cls is None:
            raise CommandError(f'Format "{self.format}" is not supported.')
        plugin = plugin_cls
        plugin.project = project
        plugin.snapshot = None
        return plugin.render()

    def _write_members_json(self, project: Project) -> None:
        """
        Dump a `members.json` file with `[{"user_id": …, "username": …, "role": …}, …]`.
        """
        payload = [
            {
                'user_id': m.user_id,
                'username': m.user.get_username(),
                'first_name': m.user.first_name,
                'last_name': m.user.last_name,
                'email': m.user.email,
                'role': m.role,
                'project_title': project.title,
                'project_site_domain': project.site.domain,
            }
            for m in project.memberships.all()
        ]

        if not payload:  # skip empty projects
            return

        target_dir = self.path / str(project.id)
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / 'members.json'

        logger.info('Writing %s', file_path)
        with file_path.open('w', encoding='utf-8') as fp:
            json.dump(payload, fp, ensure_ascii=False, indent=2)

    def _write_response(
        self,
        project: Project,
        subdir: str,
        response,
    ) -> None:
        filename = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
        if not filename:
            raise CommandError('Export response did not include a filename header.')

        target_dir = self.path / str(project.id) / subdir
        target_dir.mkdir(parents=True, exist_ok=True)

        file_path = target_dir / filename
        logger.info('Writing %s', file_path)
        with file_path.open('wb') as fp:
            fp.write(response.content)
