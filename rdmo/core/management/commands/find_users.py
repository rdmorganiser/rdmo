import csv
import re

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--id',
                            default='.*',
                            help='find users by id')
        parser.add_argument('--email',
                            default='.*',
                            help='find users by email')
        parser.add_argument('--username',
                            default='.*',
                            help='find users by username')
        parser.add_argument('--first_name',
                            default='.*',
                            help='find users by first name')
        parser.add_argument('--last_name',
                            default='.*',
                            help='find users by last name')
        parser.add_argument('-p', '--print',
                            action='store_true',
                            help='print found users, do not save them to csv')
        parser.add_argument('-o', '--output_file',
                            default='found_users.csv',
                            help='output file, default is "found_users.csv"')

    def save_csv(self, data, filename):
        if data:
            with open(filename, 'w', newline='') as data_file:
                csv_writer = csv.writer(data_file)
                csv_writer.writerow(list(data[0].keys()))
                for user in data:
                    csv_writer.writerow(user.values())
            print(f'List written to {filename}')

    def print_file(self, filename):
        with open(filename) as f:
            content = f.read()
            print(content)

    def rx_match(self, regex, s):
        return bool(re.search(regex, str(s)))

    def check_match(self, user, options):
        return all(
            self.rx_match(options[key], getattr(user, key))
            for key in ['id', 'email', 'username', 'last_name', 'first_name']
        )

    def find_users(self, options):
        return [
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
            for user in User.objects.all().order_by('date_joined')
            if self.check_match(user, options)
        ]

    def handle(self, *args, **options):
        no_total_users = User.objects.count()
        print(f'Total no of users: {no_total_users}')
        found_users = self.find_users(options)

        percentage = (100 / no_total_users) * len(found_users) if no_total_users else 0
        print(f'Matching the filter: {len(found_users)}  {percentage:.2f}%')

        self.save_csv(found_users, options['output_file'])
        if options['print']:
            self.print_file(options['output_file'])
