# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0007_data_model_refactored'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('order', 'slug'), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('order', 'slug'), 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('order', 'slug'), 'verbose_name': 'Topic', 'verbose_name_plural': 'Topics'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='title_de',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='title',
            new_name='title_de',
        ),
        migrations.RemoveField(
            model_name='question',
            name='identifier',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(default=' ', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.SlugField(default=' '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='title_en',
            field=models.CharField(default=' ', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='text_de',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='text_en',
            field=models.TextField(),
        ),
    ]
