# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_renaming'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=django_markdown.models.MarkdownField(blank=True),
        ),
    ]
