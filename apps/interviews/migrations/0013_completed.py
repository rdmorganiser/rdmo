# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0012_current_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='completed',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='interview',
            name='current_question',
            field=models.ForeignKey(to='interviews.Question', null=True),
        ),
    ]
