from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def run_data_migration(apps, schema_editor):
    View = apps.get_model('views', 'View')
    Site = apps.get_model('sites', 'Site')

    for view in View.objects.all():
        if not view.sites.exists():
            view.sites.add(Site.objects.get(pk=settings.SITE_ID))


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0022_manager'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
