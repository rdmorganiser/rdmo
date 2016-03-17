# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_valueset_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='valueset',
            name='index',
        ),
        migrations.AddField(
            model_name='valueentity',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]
