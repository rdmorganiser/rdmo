# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_detail_key_type_field_length_increased'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailkey',
            old_name='hint',
            new_name='help_text',
        ),
        migrations.AlterField(
            model_name='detailkey',
            name='options',
            field=jsonfield.fields.JSONField(blank=True, null=True, help_text='Enter valid JSON of the form [[key, label], [key, label], ...]'),
        ),
    ]
