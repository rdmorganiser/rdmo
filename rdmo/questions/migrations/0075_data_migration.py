from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    Page = apps.get_model('questions', 'Page')
    QuestionSet = apps.get_model('questions', 'QuestionSet')

    QuestionSet.objects.filter(id__in=Page.objects.values_list('id', flat=True)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0056_remove_continuation_questionset'),
        ('questions', '0074_data_migration'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
