# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_repeat_field_for_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='repeat',
        ),
    ]
