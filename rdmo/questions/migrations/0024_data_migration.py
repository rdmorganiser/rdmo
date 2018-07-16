# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def set_questionentity_is_collection(apps, schema_editor):
    Question = apps.get_model('questions', 'Question')

    for question in Question.objects.all():
        if question.value_type == 'options':
            question.value_type = 'option'

        question.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0023_option'),
        ('projects', '0019_option'),
    ]

    operations = [
        migrations.RunPython(set_questionentity_is_collection),
    ]
