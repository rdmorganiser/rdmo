# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('condition_type', models.CharField(max_length=2, choices=[('>', 'greater (>)'), ('>=', 'greater equal (>=)'), ('<', 'lesser (<)'), ('<=', 'lesser equal (<=)'), ('==', 'equal (==)'), ('!=', 'not equal (!=)')])),
                ('condition_value', models.CharField(max_length=256)),
                ('condition_question', models.ForeignKey(to='questions.Question')),
                ('group', models.ForeignKey(to='questions.Group', related_name='conditions')),
            ],
            options={
                'verbose_name': 'Condition',
                'verbose_name_plural': 'Conditions',
            },
        ),
    ]
