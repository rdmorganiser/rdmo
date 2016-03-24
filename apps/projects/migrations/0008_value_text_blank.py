# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_value_entity_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
