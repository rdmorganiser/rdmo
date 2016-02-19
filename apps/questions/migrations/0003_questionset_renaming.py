# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_refactoring'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_set',
            new_name='questionset',
        ),
        migrations.AlterField(
            model_name='section',
            name='catalog',
            field=models.ForeignKey(to='questions.Catalog', related_name='sections'),
        ),
    ]
