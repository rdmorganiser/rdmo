# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0006_attribute_fk_null'),
        ('projects', '0004_attribute_fk_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='catalog',
            field=models.ForeignKey(related_name='+', default=1, to='catalogs.Catalog'),
            preserve_default=False,
        ),
    ]
