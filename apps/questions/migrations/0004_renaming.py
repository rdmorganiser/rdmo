# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_conditions_refactored'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='condition',
            options={'ordering': ('group__subsection__section__order', 'group__subsection__order', 'group__order'), 'verbose_name_plural': 'Conditions', 'verbose_name': 'Condition'},
        ),
    ]
