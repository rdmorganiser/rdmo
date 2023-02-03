# Generated by Django 3.2.14 on 2023-01-10 14:05

from django.db import migrations, models
import django.db.models.deletion


def run_data_migration(apps, schema_editor):
    QuestionSet = apps.get_model('questions', 'QuestionSet')

    for questionset in QuestionSet.objects.all():
        if questionset.page is not None:
            questionset.page.questionsets.add(questionset)


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0085_section_pages'),
    ]

    operations = [
        # remove the related_name='questionsets' from QuestionSet.page
        migrations.AlterField(
            model_name='questionset',
            name='page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='questions.Page'),
        ),
        migrations.AddField(
            model_name='page',
            name='questionsets',
            field=models.ManyToManyField(blank=True, help_text='The question sets of this page.', related_name='pages', to='questions.QuestionSet', verbose_name='Question sets'),
        ),
        migrations.RunPython(run_data_migration),
        migrations.RemoveField(
            model_name='questionset',
            name='page',
        )
    ]