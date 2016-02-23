# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_attributes'),
        ('projects', '0002_cleanup'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='attribute',
            field=models.ForeignKey(related_name='values', default=None, to='domain.Attribute'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='valueset',
            name='attributeset',
            field=models.ForeignKey(related_name='valuesets', blank=True, to='domain.AttributeSet', null=True),
        ),
    ]
