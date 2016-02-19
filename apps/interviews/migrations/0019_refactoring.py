# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0018_order_for_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='order',
        ),
    ]
