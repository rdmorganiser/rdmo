# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_alter_current_snapshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='key',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
    ]
