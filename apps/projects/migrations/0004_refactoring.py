# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_repeat_field_for_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(editable=False, verbose_name='created')),
                ('updated', models.DateTimeField(editable=False, verbose_name='updated')),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
            },
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(editable=False, verbose_name='created')),
                ('updated', models.DateTimeField(editable=False, verbose_name='updated')),
            ],
            options={
                'verbose_name': 'Snapshot',
                'verbose_name_plural': 'Snapshots',
                'ordering': ('project', 'pk'),
            },
        ),
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(editable=False, verbose_name='created', default=datetime.datetime(2016, 2, 19, 14, 1, 50, 766103)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(editable=False, verbose_name='updated', default=datetime.datetime(2016, 2, 19, 14, 1, 56, 934815)),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, primary_key=True, to='projects.Entity', parent_link=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
            bases=('projects.entity',),
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, primary_key=True, to='projects.Entity', parent_link=True, serialize=False)),
                ('text', models.TextField()),
                ('belongs_to', models.ForeignKey(null=True, to='projects.Collection', blank=True, related_name='values')),
            ],
            options={
                'verbose_name': 'Value',
                'verbose_name_plural': 'Values',
            },
            bases=('projects.entity',),
        ),
        migrations.AddField(
            model_name='snapshot',
            name='project',
            field=models.ForeignKey(to='projects.Project', related_name='snapshots'),
        ),
        migrations.AddField(
            model_name='entity',
            name='snapshot',
            field=models.ForeignKey(to='projects.Snapshot', related_name='entities'),
        ),
        migrations.AddField(
            model_name='project',
            name='current_snapshot',
            field=models.ForeignKey(null=True, to='projects.Snapshot', blank=True, related_name='+'),
        ),
    ]
