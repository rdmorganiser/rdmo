# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Catalog',
                'verbose_name_plural': 'Catalogs',
            },
            bases=(models.Model, apps.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('relation', models.CharField(max_length=2, choices=[('>', 'greater (>)'), ('>=', 'greater equal (>=)'), ('<', 'lesser (<)'), ('<=', 'lesser equal (<=)'), ('==', 'equal (==)'), ('!=', 'not equal (!=)')])),
                ('value', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Condition',
                'verbose_name_plural': 'Conditions',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
            name='QuestionEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'QuestionEntity',
                'verbose_name_plural': 'QuestionEntities',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
                ('catalog', models.ForeignKey(related_name='section', to='questions.Catalog')),
            ],
            options={
                'verbose_name': 'Section',
                'ordering': ('order',),
                'verbose_name_plural': 'Sections',
            },
            bases=(models.Model, apps.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
                ('section', models.ForeignKey(related_name='subsections', to='questions.Section')),
            ],
            options={
                'verbose_name': 'Subsection',
                'ordering': ('section__order', 'order'),
                'verbose_name_plural': 'Subsections',
            },
            bases=(models.Model, apps.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('questionentity_ptr', models.OneToOneField(serialize=False, to='questions.QuestionEntity', auto_created=True, primary_key=True, parent_link=True)),
                ('text_en', models.TextField()),
                ('text_de', models.TextField()),
                ('widget_type', models.CharField(max_length=12, choices=[('text', 'Text'), ('textarea', 'Textarea'), ('yesno', 'Yes/No'), ('checkbox', 'Checkboxes'), ('radio', 'Radio buttons'), ('select', 'Select'), ('multiselect', 'Multiselect'), ('slider', 'Slider'), ('list', 'List')])),
            ],
            options={
                'verbose_name': 'Question',
                'ordering': ('subsection__section__order', 'subsection__order', 'order'),
                'verbose_name_plural': 'Questions',
            },
            bases=('questions.questionentity', apps.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('questionentity_ptr', models.OneToOneField(serialize=False, to='questions.QuestionEntity', auto_created=True, primary_key=True, parent_link=True)),
            ],
            options={
                'verbose_name': 'QuestionSet',
                'verbose_name_plural': 'QuestionSets',
            },
            bases=('questions.questionentity',),
        ),
        migrations.AddField(
            model_name='questionentity',
            name='subsection',
            field=models.ForeignKey(related_name='entities', to='questions.Subsection'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_set',
            field=models.ForeignKey(to='questions.QuestionSet', null=True, related_name='questions', blank=True),
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(related_name='options', to='questions.Question'),
        ),
        migrations.AddField(
            model_name='condition',
            name='question',
            field=models.ForeignKey(related_name='conditions', to='questions.Question'),
        ),
        migrations.AddField(
            model_name='condition',
            name='source',
            field=models.ForeignKey(related_name='+', to='questions.Question'),
        ),
    ]
