# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_initial_after_reset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='additional_input',
            field=models.BooleanField(default=False),
        ),
    ]
