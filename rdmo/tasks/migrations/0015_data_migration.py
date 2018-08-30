# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    Timeframe = apps.get_model('tasks', 'Timeframe')

    # migrate questionsets
    for task in Task.objects.all():
        try:
            task.start_attribute = task.timeframe.start_attribute
            task.end_attribute = task.timeframe.end_attribute
            task.days_before = task.timeframe.days_before
            task.days_after = task.timeframe.days_after
            task.save()

        except Timeframe.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_move_timeframe_to_task'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
