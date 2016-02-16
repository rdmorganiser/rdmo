# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_conditions_refactored'),
        ('interviews', '0015_questions_moved'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='skipped_groups',
            field=models.ManyToManyField(related_name='interviews_skipped', to='questions.Group'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='current_group',
            field=models.ForeignKey(related_name='interviews_current', to='questions.Group', null=True),
        ),
    ]
