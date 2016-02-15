# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0014_current_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='subsection',
        ),
        migrations.RemoveField(
            model_name='question',
            name='group',
        ),
        migrations.RemoveField(
            model_name='question',
            name='options',
        ),
        migrations.RemoveField(
            model_name='subsection',
            name='section',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='questions.Question'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='current_group',
            field=models.ForeignKey(null=True, to='questions.Group'),
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Option',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.DeleteModel(
            name='Subsection',
        ),
    ]
