# Generated by Django 4.2.8 on 2024-08-15 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0060_alter_issue_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='visibility',
            field=models.CharField(choices=[('private', 'Private'), ('internal', 'Internal')], default='private', help_text='The visibility for this project.', max_length=8, verbose_name='visibility'),
        ),
    ]
