# Generated by Django 3.2.19 on 2023-06-29 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0027_view_editors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='view',
            options={'ordering': ('uri',), 'verbose_name': 'View', 'verbose_name_plural': 'Views'},
        ),
        migrations.RenameField(
            model_name='view',
            old_name='key',
            new_name='uri_path',
        ),
        migrations.AlterField(
            model_name='view',
            name='uri',
            field=models.URLField(blank=True, help_text='The Uniform Resource Identifier of this view (auto-generated).', max_length=800, verbose_name='URI'),
        ),
        migrations.AlterField(
            model_name='view',
            name='uri_path',
            field=models.SlugField(blank=True, help_text='The path for the URI of this view.', max_length=512, verbose_name='URI Path'),
        ),
    ]
