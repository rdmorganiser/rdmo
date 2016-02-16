# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0016_skipped_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interview',
            name='skipped_groups',
        ),
        migrations.AlterField(
            model_name='interview',
            name='current_group',
            field=models.ForeignKey(to='questions.Group', blank=True, null=True),
        ),
    ]
