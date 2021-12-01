import csv
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rdmo.projects.models import Membership


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--output_file', default='potential_spam_users.csv',
            help='output file, default is \'potential_spam_users.csv\''
        )
        parser.add_argument(
            '-t', '--timespan', default=2, type=int,
            help='timespan in seconds between two joining users, ' +
            'less than the given value is considered to be suspicious ' +
            ', default is 2'
        )
        parser.add_argument(
            '-n', '--occurence', default=3, type=int,
            help='number of sequentially occuring timespan ' +
            'violations at which users are put into the ' +
            'potential spam users list, default is 3'
        )

    def rm(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

    def save_csv(self, data, filename):
        self.rm(filename)
        data_file = open(filename, 'w')
        csv_writer = csv.writer(data_file)
        for el in data:
            group = data[el]
            for user in group:
                csv_writer.writerow(user.values())
        print('List written to ' + filename)

    def get_users_having_projects(self):
        arr = []
        memberships = Membership.objects.all().values_list('user')
        for mem in memberships:
            arr.append(
                User.objects.filter(id=mem[0]).values('id')[0]['id']
            )
        return arr

    def append_to_group(self, group_list, group_count, user, list_users_having_projects):
        date_string = '%Y-%m-%dT%H:%M:%S.%f'
        last_login = user['last_login']
        if last_login is not None:
            last_login = last_login.strftime(date_string)

        has_project = user['id'] in list_users_having_projects
        group_list[group_count].append(
            {
                'id': user['id'],
                'email': user['email'],
                'username': user['username'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'date_joined': user['date_joined'].strftime(date_string),
                'last_login': last_login,
                'has_project': has_project,
            }
        )
        return group_list

    def handle(self, *args, **options):

        list_users_having_projects = self.get_users_having_projects()
        no_users_having_projects = 0

        arr = []
        no_total_users = User.objects.all().count()
        print('Total no of users:    %d' % (no_total_users))
        for idx, user in enumerate(User.objects.all().order_by('date_joined')):
            arr.append(
                {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'date_joined': user.date_joined,
                    'unix_joined': user.date_joined.timestamp(),
                    'email': user.email,
                    'last_login': user.last_login,
                }
            )

        grouped = {}
        group_count = 0
        for idx, user in enumerate(arr):
            prev = None
            diff = options['timespan']
            if idx > 0:
                prev = arr[idx-1]
                diff = user['unix_joined'] - prev['unix_joined']

            if prev is not None and diff >= options['timespan']:
                group_count += 1

            try:
                grouped[group_count]
            except KeyError:
                grouped[group_count] = []

            grouped = self.append_to_group(
                grouped, group_count, user, list_users_having_projects
            )

        no_potential_spam_users = 0
        grouped_clean = {}
        for group_id in grouped:
            group = grouped[group_id]
            if len(group) > options['occurence']:
                no_potential_spam_users += len(group)
                grouped_clean[group_id] = group

        print(
            'Potential spam users: %d  %.2f%% / of which have at least one project %d'
            % (
                no_potential_spam_users,
                (100/no_total_users)*no_potential_spam_users,
                no_users_having_projects
            )
        )

        self.save_csv(grouped_clean, options['output_file'])
