# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0004_verbosename'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attributeentity',
            options={'ordering': ('full_title',), 'verbose_name': 'AttributeEntity', 'verbose_name_plural': 'AttributeEntities'},
        ),
    ]
