# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_questionset_renaming'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionentity',
            options={'verbose_name': 'QuestionEntity', 'verbose_name_plural': 'QuestionEntities', 'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='subsection',
            options={'verbose_name': 'Subsection', 'verbose_name_plural': 'Subsections', 'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='questionset',
            name='title_de',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionset',
            name='title_en',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
