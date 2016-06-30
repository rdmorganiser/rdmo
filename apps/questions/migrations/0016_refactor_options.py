# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0015_primary_attribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='input_field',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='option',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
