from django.conf import settings
from django.db import migrations


def set_sites_for_catalogs_without_sites(apps, schema_editor):
    if not settings.MULTISITE:
        return

    Catalog = apps.get_model('questions', 'Catalog')
    Site = apps.get_model('sites', 'Site')

    all_sites = Site.objects.all()
    if not all_sites.exists():
        return

    catalogs_without_sites = (
        Catalog.objects
        .filter(sites__isnull=True)
        .distinct()
    )

    for catalog in catalogs_without_sites:
        catalog.sites.set(all_sites)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0097_alter_question_widget_type'),
    ]

    operations = [
        migrations.RunPython(
            set_sites_for_catalogs_without_sites,
            migrations.RunPython.noop,
        ),
    ]
