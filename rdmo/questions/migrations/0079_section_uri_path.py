# Generated by Django 3.2.14 on 2023-01-16 13:32

from django.db import migrations, models


def run_data_migration(apps, schema_editor):
    Section = apps.get_model('questions', 'Section')

    for section in Section.objects.all():
        section.uri_path = '%s/%s' % (section.catalog.uri_path, section.key)
        section.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0078_catalog_uri_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='path',
            new_name='uri_path',
        ),
        migrations.AlterField(
            model_name='section',
            name='uri',
            field=models.URLField(blank=True, help_text='The Uniform Resource Identifier of this section (auto-generated).', max_length=800, verbose_name='URI'),
        ),
        migrations.AlterField(
            model_name='section',
            name='uri_path',
            field=models.CharField(blank=True, help_text='The part for the URI of this section.', max_length=512, verbose_name='Label'),
        ),
        migrations.RunPython(run_data_migration),
        migrations.RemoveField(
            model_name='section',
            name='key',
        ),
    ]
