# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='attributeset',
            field=models.ForeignKey(to='domain.AttributeSet', related_name='attributes', null=True, blank=True, help_text='optional'),
        ),
    ]
