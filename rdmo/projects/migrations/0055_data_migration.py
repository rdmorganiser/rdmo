from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    Continuation = apps.get_model('projects', 'Continuation')

    for continuation in Continuation.objects.all():
        continuation.page_id = continuation.questionset_id
        continuation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0054_continuation_page'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
