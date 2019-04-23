# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import rdmo.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0003_condition'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerboseName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(max_length=256)),
                ('name_de', models.CharField(max_length=256)),
                ('name_plural_en', models.CharField(max_length=256)),
                ('name_plural_de', models.CharField(max_length=256)),
                ('attribute_entity', models.OneToOneField(to='domain.AttributeEntity', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'VerboseName',
                'verbose_name_plural': 'VerboseNames',
            },
            bases=(models.Model, rdmo.core.models.TranslationMixin),
        ),
    ]
