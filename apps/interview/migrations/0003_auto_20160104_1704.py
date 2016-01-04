# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_auto_20160104_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='previous',
            field=models.ForeignKey(null=True, to='interview.Question', blank=True),
        ),
    ]
