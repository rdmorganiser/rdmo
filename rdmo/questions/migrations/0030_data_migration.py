# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    QuestionSet = apps.get_model('questions', 'QuestionSet')
    Question = apps.get_model('questions', 'Question')
    VerboseName = apps.get_model('domain', 'VerboseName')
    Range = apps.get_model('domain', 'Range')

    for questionset in QuestionSet.objects.exclude(attribute_entity=None):
        try:
            verbose_name = questionset.attribute_entity.verbosename

            questionset.verbose_name_en = verbose_name.name_en
            questionset.verbose_name_de = verbose_name.name_de
            questionset.verbose_name_plural_en = verbose_name.name_plural_en
            questionset.verbose_name_plural_de = verbose_name.name_plural_de
            questionset.save()

        except VerboseName.DoesNotExist:
            pass

    for question in Question.objects.all():
        try:
            verbose_name = question.attribute_entity.verbosename

            question.verbose_name_en = verbose_name.name_en
            question.verbose_name_de = verbose_name.name_de
            question.verbose_name_plural_en = verbose_name.name_plural_en
            question.verbose_name_plural_de = verbose_name.name_plural_de
            question.save()

        except VerboseName.DoesNotExist:
            pass

        try:
            range = question.attribute_entity.attribute.range

            question.minimum = range.minimum
            question.maximum = range.maximum
            question.step = range.step
            question.save()

        except Range.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0029_verbose_name_and_range'),
        ('domain', '0035_remove_is_collection_and_parent_collection')
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
