# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion

import rdmo.core.models

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('full_title', models.CharField(max_length=256)),
                ('description', models.TextField(null=True, blank=True)),
                ('uri', models.URLField(null=True, blank=True)),
                ('is_collection', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'AttributeEntity',
                'verbose_name_plural': 'AttributeEntities',
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relation', models.CharField(max_length=8, choices=[('eq', 'equal (==)'), ('neq', 'not equal (!=)'), ('contains', 'contains'), ('gt', 'greater than (>)'), ('gte', 'greater than or equal (>=)'), ('lt', 'lesser than (<)'), ('lte', 'lesser than or equal (<=)')])),
                ('target_text', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Condition',
                'verbose_name_plural': 'Conditions',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(null=True)),
                ('text_en', models.CharField(max_length=256)),
                ('text_de', models.CharField(max_length=256)),
                ('additional_input', models.BooleanField()),
            ],
            options={
                'ordering': ('attribute', 'order'),
                'verbose_name': 'Option',
                'verbose_name_plural': 'Options',
            },
            bases=(models.Model, rdmo.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Range',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minimum', models.FloatField()),
                ('maximum', models.FloatField()),
                ('step', models.FloatField()),
            ],
            options={
                'ordering': ('attribute',),
                'verbose_name': 'Range',
                'verbose_name_plural': 'Ranges',
            },
            bases=(models.Model, rdmo.core.models.TranslationMixin),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('attributeentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='domain.AttributeEntity', on_delete=models.CASCADE)),
                ('value_type', models.CharField(max_length=8, choices=[('text', 'Text'), ('integer', 'Integer'), ('float', 'Float'), ('boolean', 'Boolean'), ('datetime', 'Datetime'), ('options', 'Options')])),
                ('unit', models.CharField(max_length=64, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
            bases=('domain.attributeentity',),
        ),
        migrations.AddField(
            model_name='condition',
            name='target_option',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='domain.Option', null=True),
        ),
        migrations.AddField(
            model_name='attributeentity',
            name='parent_entity',
            field=models.ForeignKey(related_name='children', blank=True, to='domain.AttributeEntity', help_text='optional', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='range',
            name='attribute',
            field=models.OneToOneField(to='domain.Attribute', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='option',
            name='attribute',
            field=models.ForeignKey(related_name='options', to='domain.Attribute', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='condition',
            name='attribute',
            field=models.ForeignKey(related_name='conditions', to='domain.Attribute', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='condition',
            name='source_attribute',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='domain.Attribute', null=True),
        ),
    ]
