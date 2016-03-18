# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_new_app_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='title_de',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='title_en',
            field=models.CharField(max_length=256),
        ),
    ]
