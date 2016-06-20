# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial_after_reset'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questionentity',
            options={'ordering': ('subsection__section__catalog__order', 'subsection__section__order', 'subsection__order', 'order'), 'verbose_name': 'QuestionEntity', 'verbose_name_plural': 'QuestionEntities'},
        ),
    ]
