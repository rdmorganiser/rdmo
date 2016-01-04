# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0003_auto_20160104_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='identifier',
            field=models.CharField(max_length=16, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('textarea', 'Textarea'), ('checkbox', 'Checkbox'), ('radio', 'Radio button'), ('select', 'Select'), ('multiselect', 'Multiselect'), ('slider', 'Slider'), ('list', 'List')], max_length=11),
        ),
    ]
