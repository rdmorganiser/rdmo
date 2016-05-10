# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0005_remove_registration'),
        ('questions', '0014_alter_widget_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionset',
            name='primary_attribute',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='domain.Attribute', null=True),
        ),
    ]
