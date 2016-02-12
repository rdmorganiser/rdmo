# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0010_section_subsection_renaming'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(null=True)),
                ('title_en', models.CharField(max_length=256)),
                ('title_de', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('subsection__section__order', 'subsection__order', 'order'),
                'verbose_name_plural': 'Subsections',
                'verbose_name': 'Subsection',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('key', models.SlugField()),
                ('text_en', models.CharField(max_length=256)),
                ('text_de', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('key',),
                'verbose_name_plural': 'Options',
                'verbose_name': 'Option',
            },
        ),
        migrations.RemoveField(
            model_name='jump',
            name='condition_question',
        ),
        migrations.RemoveField(
            model_name='jump',
            name='target',
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('group__subsection__section__order', 'group__subsection__order', 'group__order', 'order'), 'verbose_name_plural': 'Questions', 'verbose_name': 'Question'},
        ),
        migrations.AlterModelOptions(
            name='subsection',
            options={'ordering': ('section__order', 'order'), 'verbose_name_plural': 'Subsections', 'verbose_name': 'Subsection'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='subsection',
        ),
        migrations.RemoveField(
            model_name='question',
            name='options',
        ),
        migrations.DeleteModel(
            name='Jump',
        ),
        migrations.AddField(
            model_name='group',
            name='subsection',
            field=models.ForeignKey(to='interviews.Subsection', related_name='groups'),
        ),
        migrations.AddField(
            model_name='question',
            name='group',
            field=models.ForeignKey(default=1, to='interviews.Group', related_name='questions'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='options',
            field=models.ManyToManyField(null=True, to='interviews.Option', blank=True),
        ),
    ]
