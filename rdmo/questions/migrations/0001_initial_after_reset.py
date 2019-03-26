# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import rdmo.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_initial_after_reset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Catalog',
                'verbose_name_plural': 'Catalogs',
            },
            bases=(models.Model, rdmo.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='QuestionEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
                ('help_en', models.TextField(null=True, blank=True)),
                ('help_de', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('subsection__section__catalog__order', 'subsection__section__order', 'subsection__order'),
                'verbose_name': 'QuestionEntity',
                'verbose_name_plural': 'QuestionEntities',
            },
            bases=(models.Model, rdmo.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
                ('catalog', models.ForeignKey(related_name='sections', to='questions.Catalog', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('catalog__order', 'order'),
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
            bases=(models.Model, rdmo.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
                ('section', models.ForeignKey(related_name='subsections', to='questions.Section', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('section__catalog__order', 'section__order', 'order'),
                'verbose_name': 'Subsection',
                'verbose_name_plural': 'Subsections',
            },
            bases=(models.Model, rdmo.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('questionentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='questions.QuestionEntity', on_delete=models.CASCADE)),
                ('text_en', models.TextField()),
                ('text_de', models.TextField()),
                ('widget_type', models.CharField(max_length=12, choices=[('text', 'Text'), ('textarea', 'Textarea'), ('yesno', 'Yes/No'), ('checkbox', 'Checkboxes'), ('radio', 'Radio buttons'), ('select', 'Select drop-down'), ('range', 'Range slider'), ('date', 'Date picker')])),
            ],
            options={
                'ordering': ('subsection__section__catalog__order', 'subsection__section__order', 'subsection__order'),
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
            bases=('questions.questionentity',),
        ),
        migrations.AddField(
            model_name='questionentity',
            name='attribute_entity',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='domain.AttributeEntity', null=True),
        ),
        migrations.AddField(
            model_name='questionentity',
            name='subsection',
            field=models.ForeignKey(related_name='entities', to='questions.Subsection', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='question',
            name='parent_entity',
            field=models.ForeignKey(related_name='questions', blank=True, to='questions.QuestionEntity', null=True, on_delete=models.CASCADE),
        ),
    ]
