# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_conditions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='condition',
            old_name='condition_question',
            new_name='question',
        ),
        migrations.RenameField(
            model_name='condition',
            old_name='condition_type',
            new_name='relation',
        ),
        migrations.RenameField(
            model_name='condition',
            old_name='condition_value',
            new_name='value',
        ),
    ]
