# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0008_data_model_refactored'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('order',), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('category__topic__order', 'category__order', 'order'), 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('order',), 'verbose_name': 'Topic', 'verbose_name_plural': 'Topics'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='next',
        ),
    ]
