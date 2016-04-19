# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0004_text_moved_to_question_entity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attribute',
            options={'ordering': ('attributeset', 'tag'), 'verbose_name': 'Attribute', 'verbose_name_plural': 'Attributes'},
        ),
    ]
