import csv
import re

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rdmo.projects.models import Membership


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--id', default='.*',
            help='find users by id'
        )
        parser.add_argument(
            '--email', default='.*',
            help='find users by email'
        )
        parser.add_argument(
            '--username', default='.*',
            help='find users by username'
        )
        parser.add_argument(
            '--first_name', default='.*',
            help='find users by first name'
        )
        parser.add_argument(
            '--last_name', default='.*',
            help='find users by last name'
        )
        parser.add_argument(
            '-p', '--print',  action='store_true',
            help='print found users, don\'t save them to csv'
        )
        parser.add_argument(
            '-o', '--output_file', default='found_users.csv',
            help='output file, default is \'found_users.csv\''
        )

    def save_csv(self, data, filename):
        if len(data) > 0:
            data_file = open(filename, 'w')
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(list(data[0].keys()))
            for user in data:
                csv_writer.writerow(user.values())
            print('List written to ' + filename)

    def print_file(self, filename):
        f = open(filename)
        content = f.read()
        print(content)
        f.close()

    def get_users_having_projects(self):
        arr = []
        memberships = Membership.objects.all().values_list('user')
        for mem in memberships:
            arr.append(
                User.objects.filter(id=mem[0]).values('id')[0]['id']
            )
        return arr

    def rx_match(self, regex, s):
        return bool(re.search(regex, str(s)))

    def check_match(self, user, options):
        if self.rx_match(options['id'], user.id) is False:
            return False
        if self.rx_match(options['email'], user.email) is False:
            return False
        if self.rx_match(options['username'], user.username) is False:
            return False
        if self.rx_match(options['last_name'], user.last_name) is False:
            return False
        if self.rx_match(options['first_name'], user.first_name) is False:
            return False
        return True

    def find_users(self, options):
        found_users = []
        for _, user in enumerate(User.objects.all().order_by('date_joined')):
            m = self.check_match(user, options)
            if m is True:
                found_users.append(
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
        return found_users

    def handle(self, *args, **options):
        no_total_users = User.objects.all().count()
        print('Total no of users:    %d' % (no_total_users))
        found_users = self.find_users(options)

        print(
            'Matching the filter:  %d  %.2f%%'
            % (
                len(found_users),
                (100/no_total_users)*len(found_users)
            )
        )

        self.save_csv(found_users, options['output_file'])
        if options['print'] is True:
            self.print_file(options['output_file'])
