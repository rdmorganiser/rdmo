# Generated by Django 3.2.16 on 2023-02-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('views', '0026_view_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='view',
            name='editors',
            field=models.ManyToManyField(blank=True, help_text='The sites that can edit this view (in a multi site setup).', related_name='view_editors', to='sites.Site', verbose_name='Editors'),
        ),
    ]
