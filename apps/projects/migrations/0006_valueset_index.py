# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_catalog'),
    ]

    operations = [
        migrations.AddField(
            model_name='valueset',
            name='index',
            field=models.IntegerField(unique=True, default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='catalog',
            field=models.ForeignKey(to='catalogs.Catalog', help_text='The catalog which will be used for this project.', related_name='+'),
        ),
    ]
