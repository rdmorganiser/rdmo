# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_is_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionset',
            name='title_de',
        ),
        migrations.RemoveField(
            model_name='questionset',
            name='title_en',
        ),
        migrations.AddField(
            model_name='questionentity',
            name='title_de',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='questionentity',
            name='title_en',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
