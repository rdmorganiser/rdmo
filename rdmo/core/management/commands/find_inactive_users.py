import sys
import csv

from datetime import datetime

import pytz

from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Greatest
from django.core.management.base import BaseCommand


from rdmo.projects.models import Project, Value


class Command(BaseCommand):

    columns = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login')

    def add_arguments(self, parser):
        parser.add_argument('since',
                            type=lambda s: pytz.utc.localize(datetime.strptime(s, '%Y-%m-%d')),
                            help='Date since the users have been inactive.')
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
