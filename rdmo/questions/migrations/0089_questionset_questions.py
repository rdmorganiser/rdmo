# Generated by Django 3.2.14 on 2023-01-10 14:05

import django.db.models.deletion
from django.db import migrations, models


def run_data_migration(apps, schema_editor):
    Question = apps.get_model('questions', 'Question')
    QuestionSetQuestion = apps.get_model('questions', 'QuestionSetQuestion')

    for question in Question.objects.exclude(questionset=None):
        QuestionSetQuestion(
            questionset=question.questionset,
            question=question,
            order=question.order,
        ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0088_questionset_questionsets'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionSetQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('questionset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionset_questions', to='questions.questionset')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_questionsets', to='questions.question')),
            ],
            options={
                'ordering': ('questionset', 'order'),
            },
        ),
        # remove the related_name='questions' from Question.page
        migrations.AlterField(
            model_name='question',
            name='questionset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='questions.QuestionSet'),
        ),
        migrations.AddField(
            model_name='questionset',
            name='questions',
            field=models.ManyToManyField(blank=True, help_text='The questions of this question set.', related_name='questionsets', through='questions.QuestionSetQuestion', to='questions.Question', verbose_name='Questions'),
        ),
        migrations.RunPython(run_data_migration),
        migrations.RemoveField(
            model_name='question',
            name='questionset',
        ),
        migrations.RemoveField(
            model_name='question',
            name='order',
        )
    ]