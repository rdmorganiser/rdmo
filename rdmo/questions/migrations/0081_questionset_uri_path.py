# Generated by Django 3.2.14 on 2023-01-16 14:56

from django.db import migrations, models


def run_data_migration(apps, schema_editor):
    QuestionSet = apps.get_model('questions', 'QuestionSet')

    for questionset in QuestionSet.objects.all():
        questionset.uri_path = build_uri_path(questionset)
        questionset.save()


def build_uri_path(questionset):
    if questionset.questionset is None:
        return '%s/%s' % (questionset.page.uri_path, questionset.key)
    else:
        return '%s/%s' % (build_uri_path(questionset.questionset), questionset.key)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0080_page_uri_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionset',
            old_name='path',
            new_name='uri_path',
        ),
        migrations.AlterField(
            model_name='questionset',
            name='uri',
            field=models.URLField(blank=True, help_text='The Uniform Resource Identifier of this question set (auto-generated).', max_length=800, verbose_name='URI'),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='uri_path',
            field=models.CharField(blank=True, help_text='The path for the URI of this question set.', max_length=512, verbose_name='URI Path'),
        ),
        migrations.RunPython(run_data_migration),
        migrations.RemoveField(
            model_name='questionset',
            name='key',
        ),
    ]