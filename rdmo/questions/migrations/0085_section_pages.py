# Generated by Django 3.2.14 on 2023-01-10 14:05

import django.db.models.deletion
from django.db import migrations, models


def run_data_migration(apps, schema_editor):
    Page = apps.get_model('questions', 'Page')
    SectionPage = apps.get_model('questions', 'SectionPage')

    for page in Page.objects.all():
        SectionPage(
            section=page.section,
            page=page,
            order=page.order,
        ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0084_catalog_sections'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_pages', to='questions.section')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_sections', to='questions.page')),
            ],
            options={
                'ordering': ('section', 'order'),
            },
        ),
        # remove the related_name='pages' from Section.section
        migrations.AlterField(
            model_name='page',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='questions.Section'),
        ),
        migrations.AddField(
            model_name='section',
            name='pages',
            field=models.ManyToManyField(blank=True, help_text='The pages of this section.', related_name='sections', through='questions.SectionPage', to='questions.Page', verbose_name='Pages'),
        ),
        migrations.RunPython(run_data_migration),
        migrations.RemoveField(
            model_name='page',
            name='section',
        ),
        migrations.RemoveField(
            model_name='page',
            name='order',
        )
    ]
