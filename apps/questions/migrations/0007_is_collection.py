# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_attribute_fk_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionentity',
            name='is_collection',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
