# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0013_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interview',
            name='current_question',
        ),
        migrations.AddField(
            model_name='interview',
            name='current_group',
            field=models.ForeignKey(null=True, to='interviews.Group'),
        ),
    ]
