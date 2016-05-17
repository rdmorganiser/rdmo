# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0005_remove_registration'),
        ('questions', '0016_refactor_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'ordering': ('question', 'order'), 'verbose_name': 'Option', 'verbose_name_plural': 'Options'},
        ),
        migrations.RemoveField(
            model_name='condition',
            name='source',
        ),
        migrations.AddField(
            model_name='condition',
            name='attribute',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='domain.Attribute', null=True),
        ),
        migrations.AlterField(
            model_name='condition',
            name='relation',
            field=models.CharField(max_length=8, choices=[('eq', 'equal (==)'), ('neq', 'not equal (!=)'), ('contains', 'contains'), ('gt', 'greater than (>)'), ('gte', 'greater than or equal (>=)'), ('lt', 'lesser than (<)'), ('lte', 'lesser than or equal (<=)')]),
        ),
    ]
