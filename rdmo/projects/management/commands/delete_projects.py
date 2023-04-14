import re

from django.core.management.base import BaseCommand

from rdmo.projects.models import Project


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'id_list_file', type=str,
            help='required list of project ids to delete in plain text format, ' +
            'project ids have to be at the beginning of the line, ' +
            'supports commenting lines out: if a line does ' +
            'not start with an integer it will be skipped'
        )

    def handle(self, *args, **options):
        project_ids = set()
        with open(options['id_list_file']) as fp:
            for line in fp.readlines():
                m = re.search(r'^([0-9]+)', line)
                if m:
                    project_ids.add(int(m.group(1)))

        if input(f'You are about to delete {len(project_ids)} projects. '
                 'Are you sure? If so please enter \'yes\' to continue: ') == 'yes':
            for project in Project.objects.filter(id__in=project_ids):
                project.delete()
                print(f'Project {project} deleted.')
        else:
            print('Aborted!')
