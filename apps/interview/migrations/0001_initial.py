# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text_en', models.TextField(blank=True)),
                ('text_de', models.TextField(blank=True)),
                ('type', models.CharField(max_length=11, choices=[('text', 'Text'), ('textarea', 'Textarea'), ('checkbox', 'Checkbox'), ('radio', 'Radio button'), ('select', 'Select'), ('multiselect', 'Multiselect')])),
                ('options', jsonfield.fields.JSONField(blank=True, help_text='Enter valid JSON of the form [[key, label], [key, label], ...]', null=True)),
                ('previous', models.ForeignKey(to='interview.Question')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
    ]
