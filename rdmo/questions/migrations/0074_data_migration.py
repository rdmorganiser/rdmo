from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    Page = apps.get_model('questions', 'Page')
    QuestionSet = apps.get_model('questions', 'QuestionSet')
    Question = apps.get_model('questions', 'Question')

    # create a page for each "regular" questionset
    pages = {}
    for questionset in QuestionSet.objects.filter(questionset=None):
        data = {
            'section': questionset.section,
            'attribute': questionset.attribute
        }
        for field in questionset._meta.get_fields():
            if not field.is_relation:
                data[field.name] = getattr(questionset, field.name)
        page = Page(**data)
        page.save(force_insert=True)
        page.conditions.set(questionset.conditions.all())

        # store the pages for later
        pages[page.id] = page

    # store the page for each questionset-in-questionset which points now to a page
    for questionset in QuestionSet.objects.exclude(questionset=None):
        if questionset.questionset_id in pages:
            questionset.page = pages[questionset.questionset_id]
            questionset.questionset_id = None
            questionset.save()

    # store the page for questions
    for question in Question.objects.all():
        if question.questionset_id in pages:
            question.page = pages[question.questionset_id]
            question.questionset_id = None
            question.save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0073_question_page'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
