from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


def run_data_migration(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Task = apps.get_model('tasks', 'Task')
    View = apps.get_model('views', 'View')

    for project in Project.objects.all():
        # add all tasks to project
        tasks = Task.objects.filter(sites=settings.SITE_ID)
        for task in tasks:
            project.tasks.add(task)

        # add all views to project
        views = View.objects.filter(sites=settings.SITE_ID).filter(models.Q(catalogs=None) | models.Q(catalogs=project.catalog))
        for view in views:
            project.views.add(view)


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0031_project_tasks'),
        ('tasks', '0028_data_migration'),
        ('views', '0023_data_migration')
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
