# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_value_text_blank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='current_snapshot',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='projects.Snapshot', null=True),
        ),
    ]
