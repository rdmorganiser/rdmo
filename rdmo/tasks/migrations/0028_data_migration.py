from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    Site = apps.get_model('sites', 'Site')

    for task in Task.objects.all():
        if not task.sites.exists():
            task.sites.add(Site.objects.get_current())


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0027_manager'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
