# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-03 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionentity',
            name='label_de',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='questionentity',
            name='label_en',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='section',
            name='label_de',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='section',
            name='label_en',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='label_de',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='label_en',
            field=models.TextField(),
        ),
    ]
