# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def set_questionentity_is_collection(apps, schema_editor):
    Value = apps.get_model('projects', 'Value')

    for value in Value.objects.all():
        if value.value_type == 'options':
            value.value_type = 'option'

        value.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_option'),
        ('questions', '0023_option'),
    ]

    operations = [
        migrations.RunPython(set_questionentity_is_collection),
    ]
