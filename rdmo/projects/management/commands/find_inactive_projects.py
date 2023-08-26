import csv
import sys
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import models
from django.db.models.functions import Greatest

import pytz

from rdmo.projects.models import Project, Value


class Command(BaseCommand):

    columns = ('id', 'title', 'created', 'updated', 'last_changed')

    def add_arguments(self, parser):
        parser.add_argument('since',
                            type=lambda s: pytz.utc.localize(datetime.strptime(s, '%Y-%m-%d')),
                            help='Date since the projects have been inactive (format: 2022-12-31).')
        parser.add_argument('-o|--output-file', dest='output_file', default=None,
                            help='Store the output in a csv file.')

    def handle(self, *args, **options):
        # prepare subquery for last_changed
        last_changed_subquery = models.Subquery(
            Value.objects.filter(project=models.OuterRef('pk')).order_by('-updated').values('updated')[:1]
        )

        # prepare actual query
        rows = Project.objects.annotate(last_changed=Greatest('updated', last_changed_subquery)) \
                              .filter(last_changed__lt=options['since']) \
                              .order_by('-last_changed') \
                              .values_list(*self.columns)

        if rows:
            fp = open(options['output_file'], 'w') if options['output_file'] else sys.stdout
            csv_writer = csv.writer(fp)
            csv_writer.writerow(self.columns)
            csv_writer.writerows(rows)
            fp.close()
