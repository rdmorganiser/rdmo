# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailkey',
            name='type',
            field=models.CharField(max_length=11, choices=[('text', 'Input field'), ('textarea', 'Textarea field'), ('checkbox', 'Checkbox'), ('radio', 'Radio button'), ('select', 'Select field'), ('multiselect', 'Multiselect field')]),
        ),
    ]
