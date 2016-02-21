# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0003_fix_for_questionset'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionentity',
            name='tag',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
