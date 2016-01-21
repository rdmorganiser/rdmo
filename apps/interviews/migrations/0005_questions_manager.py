# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0004_question_refactored'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='next_question',
            field=models.ForeignKey(blank=True, to='interviews.Question', null=True, related_name='previous_questions'),
        ),
    ]
