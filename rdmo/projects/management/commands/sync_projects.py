from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from rdmo.projects.handlers.sync_utils import sync_task_or_view_to_projects
from rdmo.projects.models import Project
from rdmo.tasks.models import Task
from rdmo.views.models import View


class Command(BaseCommand):
    help = 'Synchronize tasks and/or views to projects based on their conditions'

    def add_arguments(self, parser):
        parser.add_argument('--tasks', action='store_true', help='Sync all tasks to projects')
        parser.add_argument('--views', action='store_true', help='Sync all views to projects')
        parser.add_argument('--show', action='store_true', help='Display tasks and views per project.')

    def handle(self, *args, **options):
        show = options['show']
        if not options['tasks'] and not options['views']:
            if show:
                self.show_project_tasks_and_views()
            else:
                raise CommandError('You must specify at least one of --tasks or --views')

        if options['tasks']:
            if not settings.PROJECT_TASKS_SYNC:
                raise CommandError('PROJECT_TASKS_SYNC is disabled in settings.')
            self.sync_all_tasks_or_views_to_projects(Task)
            if show and not options['views']:
                self.show_project_tasks_and_views()

        if options['views']:
            if not settings.PROJECT_VIEWS_SYNC:
                raise CommandError('PROJECT_VIEWS_SYNC is disabled in settings.')
            self.sync_all_tasks_or_views_to_projects(View)
            if show and not options['tasks']:
                self.show_project_tasks_and_views()

        if show and (options['tasks'] and options['views']):
            self.show_project_tasks_and_views()

    def sync_all_tasks_or_views_to_projects(self, model):
        queryset = model.objects.filter(available=True)
        model_name = model._meta.verbose_name_plural
        qs_count = queryset.count()

        self.stdout.write(self.style.SUCCESS(f'Starting sync for {qs_count} available {model_name}...'))
        for instance in queryset:
            self.stdout.write(f'- Syncing: {instance}')
            sync_task_or_view_to_projects(instance)

        self.stdout.write(self.style.SUCCESS(f'Finished sync for {model_name}.\n'))

    def show_project_tasks_and_views(self):
        self.stdout.write(self.style.SUCCESS('Displaying tasks and views for each project...'))

        for project in Project.objects.all():
            task_ids = sorted(project.tasks.values_list('id', flat=True))
            view_ids = sorted(project.views.values_list('id', flat=True))

            self.stdout.write(f'Project(id={project.id}) {project.title}:')
            self.stdout.write(f'  - tasks: [{", ".join(map(str, task_ids)) if task_ids else ""}]')
            self.stdout.write(f'  - views: [{", ".join(map(str, view_ids)) if view_ids else ""}]')

        self.stdout.write('')
