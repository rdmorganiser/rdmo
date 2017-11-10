# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_permission_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailkey',
            name='type',
            field=models.CharField(max_length=11, choices=[('text', 'Text'), ('textarea', 'Textarea'), ('checkbox', 'Checkbox'), ('radio', 'Radio button'), ('select', 'Select'), ('multiselect', 'Multiselect')]),
        ),
    ]
