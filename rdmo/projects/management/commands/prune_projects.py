from django.core.management.base import BaseCommand, CommandError

from rdmo.projects.models import Project


class Command(BaseCommand):
    help = 'Search and remove projects without users with specific role'

    def add_arguments(self, parser):
        parser.add_argument('--min_role', type=str, default='owner', \
            help='Minimum membership role for projects to be pruned, e.g. author ' + \
                'will remove projects without author and owner. (Default: owner)')
        parser.add_argument('--remove', action='store_true', \
            help='Set this flag to actually remove projects')

    def handle(self, *args, **options):
        roles = ['owner']
        if options['min_role'] == 'guest':
            roles.extend(['guest', 'author', 'manager'])
        elif options['min_role'] == 'author':
            roles.extend(['author', 'manager'])
        elif options['min_role'] == 'manager':
            roles.extend(['manager'])
        elif options['min_role'] != 'owner':
            raise CommandError('Role "%s" does not exist' % options['min_role'])

        candidates = Project.objects.exclude(user__memberships__role__in=roles)
        if candidates.count() == 0:
            self.stdout.write(self.style.SUCCESS('No projects without %s' % (roles)))
            return

        self.stdout.write('Found projects without %s:' % (roles))
        for proj in candidates:
            self.stdout.write('%s (id=%s)' % (proj, proj.id))
            if options['remove']:
                self.stdout.write('...removing...', ending='')
                proj.delete()
                self.stdout.write(self.style.SUCCESS('OK'))
