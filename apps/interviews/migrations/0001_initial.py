# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
                'ordering': ('interview', 'question'),
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
            options={
                'verbose_name': 'Interview',
                'verbose_name_plural': 'Interviews',
                'ordering': ('project', 'date'),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=16)),
                ('slug', models.SlugField()),
                ('text_en', models.TextField(blank=True)),
                ('text_de', models.TextField(blank=True)),
                ('answer_type', models.CharField(choices=[('bool', 'Bool'), ('string', 'String'), ('list', 'List'), ('integer', 'Integer'), ('float', 'Float')], max_length=12)),
                ('widget_type', models.CharField(choices=[('text', 'Text'), ('textarea', 'Textarea'), ('checkbox', 'Checkbox'), ('radio', 'Radio button'), ('select', 'Select'), ('multiselect', 'Multiselect'), ('slider', 'Slider'), ('list', 'List')], max_length=12)),
                ('options', jsonfield.fields.JSONField(null=True, help_text='Enter valid JSON of the form [[key, label], [key, label], ...]', blank=True)),
                ('previous', models.ForeignKey(null=True, blank=True, to='interviews.Question')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ('identifier',),
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='interview',
            field=models.ForeignKey(to='interviews.Interview'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='interviews.Question'),
        ),
    ]
