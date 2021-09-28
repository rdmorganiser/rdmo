from __future__ import unicode_literals

from django.db import migrations


def run_data_migration(apps, schema_editor):
    Attribute = apps.get_model('domain', 'Attribute')
    QuestionSet = apps.get_model('questions', 'QuestionSet')

    questionsets = QuestionSet.objects.filter(is_collection=True)
    for questionset in questionsets:
        if questionset.attribute.key != 'id':
            try:
                questionset.attribute = Attribute.objects.get(parent=questionset.attribute, key='id')
                questionset.save()
            except Attribute.DoesNotExist:
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0064_widget_type_choices'),
    ]

    operations = [
        migrations.RunPython(run_data_migration),
    ]
