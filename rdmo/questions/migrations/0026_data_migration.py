# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    QuestionEntity = apps.get_model('questions', 'QuestionEntity')
    QuestionSet = apps.get_model('questions', 'QuestionSet')
    Question = apps.get_model('questions', 'Question')
    QuestionItem = apps.get_model('questions', 'QuestionItem')

    # migrate questionsets
    for questionentity in QuestionEntity.objects.filter(question=None):
        questionset = QuestionSet(
            id=questionentity.id,
            uri=questionentity.uri,
            uri_prefix=questionentity.uri_prefix,
            key=questionentity.key,
            path=questionentity.path,
            comment=questionentity.comment,
            attribute_entity=questionentity.attribute_entity if questionentity.is_collection else None,
            subsection=questionentity.subsection,
            is_collection=questionentity.is_collection,
            order=questionentity.order,
            help_en=questionentity.help_en,
            help_de=questionentity.help_de,
            created=questionentity.created,
            updated=questionentity.updated
        )
        questionset.save()

        for condition in questionentity.conditions.all():
            questionset.conditions.add(condition)

        # migrate questions in questionsets
        for question in questionentity.questions.all():
            questionitem = QuestionItem(
                id=question.id,
                uri=question.uri,
                uri_prefix=question.uri_prefix,
                key=question.key,
                path=question.path,
                comment=question.comment,
                attribute_entity=question.attribute_entity,
                questionset=questionset,
                is_collection=question.is_collection,
                order=question.order,
                text_en=question.text_en,
                text_de=question.text_de,
                help_en=question.help_en,
                help_de=question.help_de,
                widget_type=question.widget_type,
                value_type=question.value_type,
                unit=question.unit,
                created=question.created,
                updated=question.updated
            )
            questionitem.save()

            for optionset in question.optionsets.all():
                questionitem.optionsets.add(optionset)

            for condition in question.conditions.all():
                questionitem.conditions.add(condition)


    # migrate questions without questionsets
    for question in Question.objects.filter(parent=None):
        questionset = QuestionSet(
            id=question.id,
            uri=question.uri,
            uri_prefix=question.uri_prefix,
            key=question.key,
            path=question.path,
            comment=question.comment,
            attribute_entity=None,
            subsection=question.subsection,
            is_collection=False,
            order=question.order,
            help_en='',
            help_de='',
            created=question.created,
            updated=question.updated
        )
        questionset.save()

        for condition in question.conditions.all():
            questionset.conditions.add(condition)

        questionitem = QuestionItem(
            id=question.id,
            uri=question.uri + '/' + question.key,
            uri_prefix=question.uri_prefix,
            key=question.key,
            path=question.path + '/' + question.key,
            comment=question.comment,
            attribute_entity=question.attribute_entity,
            questionset=questionset,
            is_collection=question.is_collection,
            order=0,
            text_en=question.text_en,
            text_de=question.text_de,
            help_en=question.help_en,
            help_de=question.help_de,
            widget_type=question.widget_type,
            value_type=question.value_type,
            unit=question.unit,
            created=question.created,
            updated=question.updated
        )
        questionitem.save()

        for optionset in question.optionsets.all():
            questionitem.optionsets.add(optionset)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0025_questionset_and_questionitem'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
