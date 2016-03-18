# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_attributes'),
        ('questions', '0004_question_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionentity',
            name='tag',
        ),
        migrations.AddField(
            model_name='question',
            name='attribute',
            field=models.ForeignKey(default=None, to='domain.Attribute'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionset',
            name='attributeset',
            field=models.ForeignKey(default=None, to='domain.AttributeSet'),
            preserve_default=False,
        ),
    ]
