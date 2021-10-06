from django.core.management.base import BaseCommand

from rdmo.projects.models import Project


class Command(BaseCommand):
    help = 'Search and remove projects without owner'

    def add_arguments(self, parser):
        parser.add_argument('--remove', action='store_true', \
            help='Set this flag to actually remove projects')

    def handle(self, *args, **options):
        candidates = Project.objects.exclude(user__memberships__role='owner')
        if candidates.count() == 0:
            self.stdout.write(self.style.SUCCESS('No projects without owner'))
            return

        self.stdout.write('Found projects without owner:')
        for proj in candidates:
            self.stdout.write('%s (id=%s)' % (proj, proj.id))
            if options['remove']:
                self.stdout.write('...removing...', ending='')
                proj.delete()
                self.stdout.write(self.style.SUCCESS('OK'))
