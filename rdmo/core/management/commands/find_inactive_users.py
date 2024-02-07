import csv
import sys
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

import pytz


class Command(BaseCommand):

    columns = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login')

    def add_arguments(self, parser):
        parser.add_argument('since',
                            type=lambda s: pytz.utc.localize(datetime.strptime(s, '%Y-%m-%d')),
                            help='Date since the users have been inactive (format: "2022-12-31").')
        parser.add_argument('-o|--output-file', dest='output_file', default=None,
                            help='Store the output in a csv file.')

    def handle(self, *args, **options):
        rows = User.objects.filter(last_login__lt=options['since']) \
                            .order_by('-last_login').values_list(*self.columns)

        if rows:
            fp = open(options['output_file'], 'w') if options['output_file'] else sys.stdout
            csv_writer = csv.writer(fp)
            csv_writer.writerow(self.columns)
            csv_writer.writerows(rows)
            fp.close()
