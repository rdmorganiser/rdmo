# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_title_moved_to_question_entity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionentity',
            name='is_collection',
        ),
    ]
