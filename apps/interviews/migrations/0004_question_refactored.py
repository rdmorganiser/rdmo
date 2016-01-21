# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0003_interview_refactored'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='previous',
        ),
        migrations.AddField(
            model_name='question',
            name='next_question',
            field=models.ForeignKey(null=True, to='interviews.Question', blank=True),
        ),
    ]
