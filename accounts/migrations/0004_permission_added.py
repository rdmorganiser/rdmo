# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_hint_renamed_to_help_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detailkey',
            options={'verbose_name': 'DetailKey', 'verbose_name_plural': 'DetailKeys', 'ordering': ('key',)},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'permissions': (('update_profile', 'Can update own profile'),), 'verbose_name_plural': 'Profiles', 'ordering': ('user',)},
        ),
        migrations.AlterField(
            model_name='detailkey',
            name='help_text',
            field=models.TextField(blank=True, help_text='Enter a help text to be displayed next to the input element'),
        ),
    ]
