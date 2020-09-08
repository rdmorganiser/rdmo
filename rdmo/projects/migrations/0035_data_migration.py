from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Issue = apps.get_model('projects', 'Issue')

    for project in Project.objects.all():
        # add issues for all tasks to project
        for task in project.tasks.all():
            issue = Issue(project=project, task=task)
            issue.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_issue'),
        ('tasks', '0031_related_name')
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
