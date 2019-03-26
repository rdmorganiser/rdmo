# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('key', models.SlugField()),
                ('label', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('text', 'Input field'), ('textarea', 'Textarea field'), ('checkbox', 'Checkbox'), ('radio', 'Radio button'), ('select', 'Select field'), ('multiselect', 'Multiselect field')], max_length=8)),
                ('hint', models.TextField(blank=True)),
                ('options', jsonfield.fields.JSONField(null=True, blank=True)),
                ('required', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('details', jsonfield.fields.JSONField(null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('user',),
            },
        ),
    ]
