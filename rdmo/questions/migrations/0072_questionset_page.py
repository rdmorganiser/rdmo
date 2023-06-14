# Generated by Django 3.2.14 on 2022-12-07 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0071_alter_question_questionset'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionset',
            name='page',
            field=models.ForeignKey(blank=True, help_text='The page this question set belongs to.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questionsets', to='questions.page', verbose_name='Page'),
        )
    ]
