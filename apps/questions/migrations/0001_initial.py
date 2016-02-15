# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Group',
                'ordering': ('subsection__section__order', 'subsection__order', 'order'),
                'verbose_name_plural': 'Group',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('key', models.SlugField()),
                ('text_en', models.CharField(max_length=256)),
                ('text_de', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Option',
                'ordering': ('key',),
                'verbose_name_plural': 'Options',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(null=True)),
                ('text_en', models.TextField()),
                ('text_de', models.TextField()),
                ('answer_type', models.CharField(choices=[('bool', 'Bool'), ('string', 'String'), ('list', 'List'), ('integer', 'Integer'), ('float', 'Float')], max_length=12)),
                ('widget_type', models.CharField(choices=[('text', 'Text'), ('textarea', 'Textarea'), ('yesno', 'Yes/No'), ('checkbox', 'Checkboxes'), ('radio', 'Radio buttons'), ('select', 'Select'), ('multiselect', 'Multiselect'), ('slider', 'Slider'), ('list', 'List')], max_length=12)),
                ('group', models.ForeignKey(to='questions.Group', related_name='questions')),
                ('options', models.ManyToManyField(blank=True, to='questions.Option')),
            ],
            options={
                'verbose_name': 'Question',
                'ordering': ('group__subsection__section__order', 'group__subsection__order', 'group__order', 'order'),
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Section',
                'ordering': ('order',),
                'verbose_name_plural': 'Sections',
            },
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
                ('section', models.ForeignKey(to='questions.Section', related_name='subsections')),
            ],
            options={
                'verbose_name': 'Subsection',
                'ordering': ('section__order', 'order'),
                'verbose_name_plural': 'Subsections',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='subsection',
            field=models.ForeignKey(to='questions.Subsection', related_name='groups'),
        ),
    ]
