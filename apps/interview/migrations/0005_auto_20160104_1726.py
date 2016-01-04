# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0004_auto_20160104_1723'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': 'Questions', 'ordering': ('identifier',), 'verbose_name': 'Question'},
        ),
    ]
