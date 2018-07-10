# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def set_questionentity_is_collection(apps, schema_editor):
    QuestionEntity = apps.get_model('questions', 'QuestionEntity')

    for queryset in QuestionEntity.objects.filter(question=None):
        if queryset.attribute_entity.parent_collection:
            queryset.attribute_entity = queryset.attribute_entity.parent_collection
            queryset.is_collection = True
        else:
            queryset.is_collection = queryset.attribute_entity.is_collection
        queryset.save()

    for question in QuestionEntity.objects.exclude(question=None):
        question.is_collection = question.attribute_entity.is_collection
        question.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0021_questionentity_is_collection'),
    ]

    operations = [
        migrations.RunPython(set_questionentity_is_collection),
    ]
