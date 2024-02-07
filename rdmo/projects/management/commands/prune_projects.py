from django.core.management.base import BaseCommand, CommandError

from rdmo.projects.models import Membership, Project


class Command(BaseCommand):
    help = 'Search and remove projects without users with specific role'


    def add_arguments(self, parser):
        parser.add_argument('--min_role', type=str, default='owner', \
            help='Minimum membership role for projects to be pruned, e.g. author ' + \
                'will remove projects without author, manager and owner. (Default: owner)')
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

        memberships = Membership.objects.filter(role__in=roles).values_list('pk')
        candidates = Project.objects.exclude(memberships__in=list(memberships)).distinct()

        if candidates.count() == 0:
            self.stdout.write(self.style.SUCCESS('No projects without %s' % (roles)))
            return

        self.stdout.write('Found projects without %s:' % (roles))
        for proj in candidates:
            self.stdout.write(f'{proj} (id={proj.id})')
            if options['remove']:
                self.stdout.write('...removing...', ending='')
                proj.delete()
                self.stdout.write(self.style.SUCCESS('OK'))
