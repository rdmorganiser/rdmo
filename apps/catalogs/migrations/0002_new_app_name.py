# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Catalogs',
                'verbose_name': 'Catalog',
            },
            bases=(models.Model, apps.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('relation', models.CharField(choices=[('>', 'greater (>)'), ('>=', 'greater equal (>=)'), ('<', 'lesser (<)'), ('<=', 'lesser equal (<=)'), ('==', 'equal (==)'), ('!=', 'not equal (!=)')], max_length=2)),
                ('value', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Conditions',
                'verbose_name': 'Condition',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField()),
                ('text_en', models.CharField(max_length=256)),
                ('text_de', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Options',
                'verbose_name': 'Option',
                'ordering': ('key',),
            },
        ),
        migrations.CreateModel(
            name='QuestionEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'QuestionEntities',
                'verbose_name': 'QuestionEntity',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
                ('catalog', models.ForeignKey(to='catalogs.Catalog', related_name='sections')),
            ],
            options={
                'verbose_name_plural': 'Sections',
                'verbose_name': 'Section',
                'ordering': ('order',),
            },
            bases=(models.Model, apps.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
                ('section', models.ForeignKey(to='catalogs.Section', related_name='subsections')),
            ],
            options={
                'verbose_name_plural': 'Subsections',
                'verbose_name': 'Subsection',
                'ordering': ('order',),
            },
            bases=(models.Model, apps.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('questionentity_ptr', models.OneToOneField(primary_key=True, serialize=False, to='catalogs.QuestionEntity', parent_link=True, auto_created=True)),
                ('text_en', models.TextField()),
                ('text_de', models.TextField()),
                ('widget_type', models.CharField(choices=[('text', 'Text'), ('textarea', 'Textarea'), ('yesno', 'Yes/No'), ('checkbox', 'Checkboxes'), ('radio', 'Radio buttons'), ('select', 'Select'), ('multiselect', 'Multiselect'), ('slider', 'Slider'), ('list', 'List')], max_length=12)),
            ],
            options={
                'verbose_name_plural': 'Questions',
                'verbose_name': 'Question',
                'ordering': ('subsection__section__order', 'subsection__order', 'order'),
            },
            bases=('catalogs.questionentity', apps.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('questionentity_ptr', models.OneToOneField(primary_key=True, serialize=False, to='catalogs.QuestionEntity', parent_link=True, auto_created=True)),
                ('title_en', models.TextField()),
                ('title_de', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'QuestionSets',
                'verbose_name': 'QuestionSet',
            },
            bases=('catalogs.questionentity', apps.core.models.TranslationMixin),
        ),
        migrations.AddField(
            model_name='questionentity',
            name='subsection',
            field=models.ForeignKey(to='catalogs.Subsection', related_name='entities'),
        ),
        migrations.AddField(
            model_name='question',
            name='questionset',
            field=models.ForeignKey(blank=True, null=True, to='catalogs.QuestionSet', related_name='questions'),
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(to='catalogs.Question', related_name='options'),
        ),
        migrations.AddField(
            model_name='condition',
            name='question',
            field=models.ForeignKey(to='catalogs.Question', related_name='conditions'),
        ),
        migrations.AddField(
            model_name='condition',
            name='source',
            field=models.ForeignKey(to='catalogs.Question', related_name='+'),
        ),
    ]
