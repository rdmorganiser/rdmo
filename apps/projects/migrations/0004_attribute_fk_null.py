# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='valueset',
            field=models.ForeignKey(to='projects.ValueSet', related_name='values', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='valueset',
            name='attributeset',
            field=models.ForeignKey(to='domain.AttributeSet', related_name='valuesets', on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True),
        ),
    ]
