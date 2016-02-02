# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0009_data_model_refactored'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': 'Sections',
                'verbose_name': 'Section',
            },
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
                ('section', models.ForeignKey(related_name='subsections', to='interviews.Section')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': 'Subsections',
                'verbose_name': 'Subsection',
            },
        ),
        migrations.RemoveField(
            model_name='category',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.AddField(
            model_name='question',
            name='subsection',
            field=models.ForeignKey(to='interviews.Subsection', related_name='questions', default=None),
            preserve_default=False,
        ),
    ]
