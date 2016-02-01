# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0006_many_to_many_for_questions_next'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('order', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ('order', 'title'),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Jump',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('condition_type', models.CharField(max_length=2, choices=[('>', 'greater (>)'), ('>=', 'greater equal (>=)'), ('<', 'lesser (<)'), ('<=', 'lesser equal (<=)'), ('==', 'equal (==)'), ('!=', 'not equal (!=)')])),
                ('condition_value', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('condition_question', 'condition_value'),
                'verbose_name': 'Jump',
                'verbose_name_plural': 'Jumps',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('order', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ('order', 'title'),
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.RemoveField(
            model_name='answer',
            name='previous_answer',
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='jump',
            name='condition_question',
            field=models.ForeignKey(to='interviews.Question'),
        ),
        migrations.AddField(
            model_name='jump',
            name='target',
            field=models.ForeignKey(related_name='jumps', to='interviews.Question'),
        ),
        migrations.AddField(
            model_name='category',
            name='topic',
            field=models.ForeignKey(related_name='categories', to='interviews.Topic'),
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(related_name='questions', default=1, to='interviews.Category'),
            preserve_default=False,
        ),
    ]
