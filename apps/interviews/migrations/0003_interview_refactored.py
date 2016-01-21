# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0002_related_name_for_answer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interview',
            options={'verbose_name': 'Interview', 'verbose_name_plural': 'Interviews', 'ordering': ('project', 'updated')},
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='answer',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='interview',
            name='date',
        ),
        migrations.AddField(
            model_name='answer',
            name='created',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2016, 1, 21, 10, 12, 15, 201471, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer',
            name='previous_answer',
            field=models.ForeignKey(null=True, to='interviews.Answer'),
        ),
        migrations.AddField(
            model_name='answer',
            name='updated',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2016, 1, 21, 10, 12, 49, 611524, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interview',
            name='created',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2016, 1, 21, 10, 12, 54, 715782, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interview',
            name='updated',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2016, 1, 21, 10, 13, 0, 188177, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
