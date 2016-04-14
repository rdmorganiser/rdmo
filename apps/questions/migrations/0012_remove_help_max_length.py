# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_change_help_to_text_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionentity',
            name='help_de',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionentity',
            name='help_en',
            field=models.TextField(blank=True, null=True),
        ),
    ]
