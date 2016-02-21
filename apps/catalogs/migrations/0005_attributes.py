# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_attributes'),
        ('catalogs', '0004_question_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionentity',
            name='tag',
        ),
        migrations.AddField(
            model_name='question',
            name='attribute',
            field=models.ForeignKey(default=None, to='plans.Attribute'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionset',
            name='attributeset',
            field=models.ForeignKey(default=None, to='plans.AttributeSet'),
            preserve_default=False,
        ),
    ]
