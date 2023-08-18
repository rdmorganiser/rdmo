# Generated by Django 3.2.19 on 2023-06-29 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0034_task_editors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='key',
            new_name='uri_path',
        ),
        migrations.AlterField(
            model_name='task',
            name='uri',
            field=models.URLField(blank=True, help_text='The Uniform Resource Identifier of this task (auto-generated).', max_length=800, verbose_name='URI'),
        ),
        migrations.AlterField(
            model_name='task',
            name='uri_path',
            field=models.SlugField(blank=True, help_text='The path for the URI of this task.', max_length=512, verbose_name='URI Path'),
        ),
    ]