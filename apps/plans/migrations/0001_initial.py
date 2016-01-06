# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('interview', models.ForeignKey(to='interviews.Interview')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Plans',
                'ordering': ('interview', 'template'),
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
            },
        ),
        migrations.AddField(
            model_name='plan',
            name='template',
            field=models.ForeignKey(to='plans.Template'),
        ),
    ]
