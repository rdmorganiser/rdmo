# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='interview',
            field=models.ForeignKey(to='interviews.Interview', related_name='answers'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='project',
            field=models.ForeignKey(to='projects.Project', related_name='interviews'),
        ),
    ]
