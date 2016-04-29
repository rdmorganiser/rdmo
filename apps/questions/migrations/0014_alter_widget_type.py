# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_options_ordering'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='widget_type',
            field=models.CharField(max_length=12, choices=[('text', 'Text'), ('textarea', 'Textarea'), ('yesno', 'Yes/No'), ('checkbox', 'Checkboxes'), ('radio', 'Radio buttons'), ('select', 'Select drop-down'), ('range', 'Range slider'), ('date', 'Date picker')]),
        ),
    ]
