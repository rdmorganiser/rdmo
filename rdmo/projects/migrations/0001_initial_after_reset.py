# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_initial_after_reset'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0001_initial_after_reset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(help_text='You can use markdown syntax in the description.', blank=True)),
                ('catalog', models.ForeignKey(related_name='+', to='questions.Catalog', help_text='The catalog which will be used for this project.', on_delete=models.SET_NULL)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('project', models.ForeignKey(related_name='snapshots', to='projects.Project', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('project', 'pk'),
                'verbose_name': 'Snapshot',
                'verbose_name_plural': 'Snapshots',
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('set_index', models.IntegerField(default=0)),
                ('collection_index', models.IntegerField(default=0)),
                ('text', models.TextField(null=True, blank=True)),
                ('attribute', models.ForeignKey(related_name='values', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='domain.Attribute', null=True)),
                ('option', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='domain.Option', null=True)),
                ('snapshot', models.ForeignKey(related_name='values', to='projects.Snapshot', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Value',
                'verbose_name_plural': 'Values',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='current_snapshot',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='projects.Snapshot', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
