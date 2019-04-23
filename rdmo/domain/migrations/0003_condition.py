# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0002_additional_input'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condition',
            name='attribute',
        ),
        migrations.AddField(
            model_name='condition',
            name='attribute_entity',
            field=models.ForeignKey(related_name='conditions', default=None, to='domain.AttributeEntity', on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
