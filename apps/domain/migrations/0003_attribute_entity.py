# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0002_attribute_fk_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(verbose_name='created', editable=False)),
                ('updated', models.DateTimeField(verbose_name='updated', editable=False)),
                ('tag', models.SlugField()),
                ('is_collection', models.BooleanField()),
            ],
            options={
                'verbose_name': 'AttributeEntity',
                'verbose_name_plural': 'AttributeEntities',
            },
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='created',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='id',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='attributeset',
            name='created',
        ),
        migrations.RemoveField(
            model_name='attributeset',
            name='id',
        ),
        migrations.RemoveField(
            model_name='attributeset',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='attributeset',
            name='updated',
        ),
        migrations.AddField(
            model_name='attribute',
            name='unit',
            field=models.CharField(blank=True, null=True, max_length=64),
        ),
        migrations.AddField(
            model_name='attribute',
            name='value_type',
            field=models.CharField(default='text', choices=[('text', 'Text'), ('integer', 'Integer'), ('float', 'Float'), ('boolean', 'Boolean')], max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attribute',
            name='attributeentity_ptr',
            field=models.OneToOneField(auto_created=True, parent_link=True, default=None, primary_key=True, serialize=False, to='domain.AttributeEntity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attributeset',
            name='attributeentity_ptr',
            field=models.OneToOneField(auto_created=True, parent_link=True, default=None, primary_key=True, serialize=False, to='domain.AttributeEntity'),
            preserve_default=False,
        ),
    ]
