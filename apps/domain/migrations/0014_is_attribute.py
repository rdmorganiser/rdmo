# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-03 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0013_mptt'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributeentity',
            name='is_attribute',
            field=models.BooleanField(default=False),
        ),
    ]
