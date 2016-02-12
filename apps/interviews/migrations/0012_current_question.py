# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0011_refactoring'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group', 'ordering': ('subsection__section__order', 'subsection__order', 'order'), 'verbose_name_plural': 'Group'},
        ),
        migrations.AddField(
            model_name='interview',
            name='current_question',
            field=models.ForeignKey(to='interviews.Question', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.ManyToManyField(to='interviews.Option', blank=True),
        ),
    ]
