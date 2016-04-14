# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_attribute_entity'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionentity',
            name='help_de',
            field=models.CharField(null=True, blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='questionentity',
            name='help_en',
            field=models.CharField(null=True, blank=True, max_length=256),
        ),
    ]
