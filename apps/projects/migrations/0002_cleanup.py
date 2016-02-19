# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='created')),
                ('updated', models.DateTimeField(editable=False, verbose_name='updated')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, help_text='You can use markdown syntax in the description.')),
            ],
            options={
                'verbose_name_plural': 'Projects',
                'ordering': ('title',),
                'verbose_name': 'Project',
            },
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='created')),
                ('updated', models.DateTimeField(editable=False, verbose_name='updated')),
                ('project', models.ForeignKey(related_name='snapshots', to='projects.Project')),
            ],
            options={
                'verbose_name_plural': 'Snapshots',
                'ordering': ('project', 'pk'),
                'verbose_name': 'Snapshot',
            },
        ),
        migrations.CreateModel(
            name='ValueEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(editable=False, verbose_name='created')),
                ('updated', models.DateTimeField(editable=False, verbose_name='updated')),
            ],
            options={
                'verbose_name_plural': 'ValueEntities',
                'verbose_name': 'ValueEntity',
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('valueentity_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='projects.ValueEntity', serialize=False, parent_link=True)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Values',
                'verbose_name': 'Value',
            },
            bases=('projects.valueentity',),
        ),
        migrations.CreateModel(
            name='ValueSet',
            fields=[
                ('valueentity_ptr', models.OneToOneField(primary_key=True, auto_created=True, to='projects.ValueEntity', serialize=False, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'ValueSet',
                'verbose_name': 'ValueSet',
            },
            bases=('projects.valueentity',),
        ),
        migrations.AddField(
            model_name='valueentity',
            name='snapshot',
            field=models.ForeignKey(related_name='entities', to='projects.Snapshot'),
        ),
        migrations.AddField(
            model_name='project',
            name='current_snapshot',
            field=models.ForeignKey(related_name='+', null=True, to='projects.Snapshot', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='value',
            name='valueset',
            field=models.ForeignKey(related_name='values', null=True, to='projects.ValueSet', blank=True),
        ),
    ]
