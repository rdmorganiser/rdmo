# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0005_questions_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='next_question',
        ),
        migrations.AddField(
            model_name='question',
            name='next',
            field=models.ManyToManyField(blank=True, to='interviews.Question', related_name='previous'),
        ),
    ]
