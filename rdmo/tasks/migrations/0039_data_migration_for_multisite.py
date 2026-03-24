from django.conf import settings
from django.db import migrations


def set_sites_for_tasks_without_sites(apps, schema_editor):
    if not settings.MULTISITE:
        return

    Task = apps.get_model('tasks', 'Task')
    Site = apps.get_model('sites', 'Site')

    all_sites = Site.objects.all()
    if not all_sites.exists():
        return

    tasks_without_sites = (
        Task.objects
        .filter(sites__isnull=True)
        .distinct()
    )

    for task in tasks_without_sites:
        task.sites.set(all_sites)


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0038_alter_task_uri_path'),
    ]

    operations = [
        migrations.RunPython(
            set_sites_for_tasks_without_sites,
            migrations.RunPython.noop,
        ),
    ]