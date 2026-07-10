import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, models


class LegacyOptionSet(models.Model):
    uri = models.URLField(max_length=800, blank=True)
    uri_prefix = models.URLField(max_length=256)
    uri_path = models.CharField(max_length=512, blank=True)
    provider_key = models.CharField(max_length=128, blank=True)

    class Meta:
        app_label = 'legacy_dump'
        managed = False
        db_table = 'options_optionset'

    def __str__(self):
        return self.uri


class LegacyIntegration(models.Model):
    project_id = models.IntegerField()
    provider_key = models.CharField(max_length=128, blank=True)

    class Meta:
        app_label = 'legacy_dump'
        managed = False
        db_table = 'projects_integration'

    def __str__(self):
        return f'{self.project_id} / {self.provider_key}'


class Command(BaseCommand):
    help = 'Dump legacy provider_key assignments with matching legacy plugin settings.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-o',
            '--output',
            default='dumps/legacy_plugin_assignments.json',
            help='Write the report to this file.',
        )

    def handle(self, *args, **options):
        report = self.get_report()
        output_path = Path(options['output'])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2) + '\n')

        self.stdout.write(self.style.SUCCESS(f'created: {output_path}'))

    def get_report(self):
        return {
            'optionsets': self.add_legacy_plugins(
                self.get_optionsets(),
                self.get_legacy_plugins('OPTIONSET_PROVIDERS'),
            ),
            'integrations': self.add_legacy_plugins(
                self.get_integrations(),
                self.get_legacy_plugins('PROJECT_ISSUE_PROVIDERS'),
            ),
        }

    def add_legacy_plugins(self, rows, legacy_plugins):
        return [
            {
                **row,
                'legacy_plugin': legacy_plugins.get(row['provider_key']),
            }
            for row in rows
        ]

    def get_legacy_plugins(self, setting_name):
        return {
            key: {
                'key': key,
                'label': str(label),
                'python_path': python_path,
            }
            for key, label, python_path in getattr(settings, setting_name, [])
        }

    def get_optionsets(self):
        return self.fetch_rows(
            LegacyOptionSet,
            ('id', 'uri', 'uri_prefix', 'uri_path', 'provider_key'),
        )

    def get_integrations(self):
        return self.fetch_rows(
            LegacyIntegration,
            ('id', 'project_id', 'provider_key'),
        )

    def fetch_rows(self, model, fields):
        if not self.has_fields(model, fields):
            return []

        return list(
            model.objects
            .exclude(provider_key='')
            .order_by('id')
            .values(*fields)
        )

    def has_fields(self, model, fields):
        table_name = model._meta.db_table
        with connection.cursor() as cursor:
            if table_name not in connection.introspection.table_names(cursor):
                return False

            table_columns = {
                column.name
                for column in connection.introspection.get_table_description(cursor, table_name)
            }
            return set(fields).issubset(table_columns)
