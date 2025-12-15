from django.conf import settings
from django.db import migrations


def set_sites_for_views_without_sites(apps, schema_editor):
    if not settings.MULTISITE:
        return

    View = apps.get_model('views', 'View')
    Site = apps.get_model('sites', 'Site')

    all_sites = Site.objects.all()
    if not all_sites.exists():
        return

    views_without_sites = (
        View.objects
        .filter(sites__isnull=True)
        .distinct()
    )

    for view in views_without_sites:
        view.sites.set(all_sites)


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0031_alter_view_uri_path'),
    ]

    operations = [
        migrations.RunPython(
            set_sites_for_views_without_sites,
            migrations.RunPython.noop,
        ),
    ]