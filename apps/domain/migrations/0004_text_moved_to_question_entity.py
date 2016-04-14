# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0003_attribute_entity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attribute',
            options={'verbose_name': 'Attribute', 'verbose_name_plural': 'Attributes', 'ordering': ('tag',)},
        ),
        migrations.AlterModelOptions(
            name='attributeset',
            options={'verbose_name': 'AttributeSet', 'verbose_name_plural': 'AttributeSets', 'ordering': ('tag',)},
        ),
        migrations.AlterField(
            model_name='attribute',
            name='value_type',
            field=models.CharField(max_length=8, choices=[('text', 'Text'), ('integer', 'Integer'), ('float', 'Float'), ('boolean', 'Boolean'), ('datetime', 'Datetime')]),
        ),
    ]
