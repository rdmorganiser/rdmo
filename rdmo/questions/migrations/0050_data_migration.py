from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def run_data_migration(apps, schema_editor):
    Catalog = apps.get_model('questions', 'Catalog')
    Site = apps.get_model('sites', 'Site')

    for catalog in Catalog.objects.all():
        if not catalog.sites.exists():
            catalog.sites.add(Site.objects.get(pk=settings.SITE_ID))


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0049_manager'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
