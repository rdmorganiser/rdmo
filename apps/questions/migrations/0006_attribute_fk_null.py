# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='attribute',
            field=models.ForeignKey(to='domain.Attribute', related_name='questions', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='attributeset',
            field=models.ForeignKey(to='domain.AttributeSet', related_name='questionsets', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True),
        ),
    ]
