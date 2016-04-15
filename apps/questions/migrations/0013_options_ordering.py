# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_remove_help_max_length'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'ordering': ('question', 'key'), 'verbose_name_plural': 'Options', 'verbose_name': 'Option'},
        ),
    ]
