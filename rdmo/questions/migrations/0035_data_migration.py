# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from rdmo.core.utils import get_uri_prefix


def run_data_migration(apps, schema_editor):
    Section = apps.get_model('questions', 'Section')
    Subsection = apps.get_model('questions', 'Subsection')
    QuestionSet = apps.get_model('questions', 'QuestionSet')
    Question = apps.get_model('questions', 'Question')

    for questionset in QuestionSet.objects.all():
        questionset.section = questionset.subsection.section
        questionset.title_en = questionset.subsection.title_en
        questionset.title_de = questionset.subsection.title_de
        questionset.order = questionset.order + 10 * questionset.subsection.order

        questionset.key = questionset.subsection.key + '-' + questionset.key
        questionset.path = '%s/%s/%s' % (
            questionset.section.catalog.key,
            questionset.section.key,
            questionset.key
        )
        questionset.uri = get_uri_prefix(questionset) + '/questions/' + questionset.path
        questionset.save()

        for question in questionset.questions.all():
            question.path = '%s/%s/%s/%s' % (
                question.questionset.section.catalog.key,
                question.questionset.section.key,
                question.questionset.key,
                question.key
            )
            question.uri = get_uri_prefix(question) + '/questions/' + question.path
            question.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0034_move_questionset_to_section'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
