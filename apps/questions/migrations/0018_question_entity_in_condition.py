# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0017_refactor_conditions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condition',
            name='question',
        ),
        migrations.AddField(
            model_name='condition',
            name='question_entity',
            field=models.ForeignKey(related_name='conditions', default=None, to='questions.QuestionEntity'),
            preserve_default=False,
        ),
    ]
