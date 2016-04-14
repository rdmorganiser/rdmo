# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_help_for_question_entity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionentity',
            name='help_de',
            field=models.TextField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionentity',
            name='help_en',
            field=models.TextField(max_length=256, null=True, blank=True),
        ),
    ]
