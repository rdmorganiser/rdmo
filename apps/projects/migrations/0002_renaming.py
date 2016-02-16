# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('title',), 'verbose_name_plural': 'Projects', 'verbose_name': 'Project'},
        ),
        migrations.RenameField(
            model_name='project',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='project',
            name='pi',
        ),
    ]
