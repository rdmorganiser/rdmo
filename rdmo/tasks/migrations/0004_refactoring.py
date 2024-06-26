# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-27 15:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_meta'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('key',), 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AddField(
            model_name='task',
            name='comment',
            field=models.TextField(blank=True, help_text='Additional information about this task.', null=True, verbose_name='Comment'),
        ),
        migrations.AddField(
            model_name='task',
            name='key',
            field=models.SlugField(blank=True, help_text='The internal identifier of this task. The URI will be generated from this key.', max_length=128, null=True, verbose_name='Key'),
        ),
        migrations.AddField(
            model_name='task',
            name='uri',
            field=models.URLField(blank=True, help_text='The Uniform Resource Identifier of this task (auto-generated).', max_length=640, null=True, verbose_name='URI'),
        ),
        migrations.AddField(
            model_name='task',
            name='uri_prefix',
            field=models.URLField(blank=True, help_text='The prefix for the URI of this task.', max_length=256, null=True, verbose_name='URI Prefix'),
        ),
        migrations.AlterField(
            model_name='task',
            name='attribute',
            field=models.ForeignKey(blank=True, help_text='The attribute this task is referring to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='domain.Attribute', verbose_name='Attribute'),
        ),
        migrations.AlterField(
            model_name='task',
            name='conditions',
            field=models.ManyToManyField(blank=True, help_text='The list of conditions evaluated for this task.', to='conditions.Condition', verbose_name='Conditions'),
        ),
        migrations.AlterField(
            model_name='task',
            name='text_de',
            field=models.CharField(help_text='The German text for this task.', max_length=256, verbose_name='Text (de)'),
        ),
        migrations.AlterField(
            model_name='task',
            name='text_en',
            field=models.CharField(help_text='The English text for this task.', max_length=256, verbose_name='Text (en)'),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_period',
            field=models.DurationField(help_text='The the time period after this task becomes active.', verbose_name='Time period'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title_de',
            field=models.CharField(help_text='The German title for this task.', max_length=256, verbose_name='Title (de)'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title_en',
            field=models.CharField(help_text='The English title for this task.', max_length=256, verbose_name='Title (en)'),
        ),
    ]
