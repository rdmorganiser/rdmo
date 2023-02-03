# Generated by Django 3.2.14 on 2023-01-10 14:05

from django.db import migrations, models
import django.db.models.deletion


def run_data_migration(apps, schema_editor):
    Section = apps.get_model('questions', 'Section')

    for section in Section.objects.all():
        section.catalog.sections.add(section)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0083_meta'),
    ]

    operations = [
        # remove the related_name='sections' from Section.catalog
        migrations.AlterField(
            model_name='section',
            name='catalog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='questions.Catalog'),
        ),
        migrations.AddField(
            model_name='catalog',
            name='sections',
            field=models.ManyToManyField(blank=True, help_text='The sections of this catalog.', related_name='catalogs', to='questions.Section', verbose_name='Sections'),
        ),
        migrations.RunPython(run_data_migration),
        migrations.RemoveField(
            model_name='section',
            name='catalog',
        )
    ]