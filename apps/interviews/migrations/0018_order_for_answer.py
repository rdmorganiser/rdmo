# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0017_skipped_groups_removed_again'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
