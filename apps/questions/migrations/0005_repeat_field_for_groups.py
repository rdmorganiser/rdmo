# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_renaming'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='repeat',
            field=models.BooleanField(default=False),
        ),
    ]
