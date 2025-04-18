# Generated by Django 4.2.13 on 2024-07-11 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0035_alter_help_text_and_set_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='default_text_lang1',
            field=models.TextField(blank=True, default='', help_text='The default text value for the additional input of this option (in the primary language).', verbose_name='Default text value (primary)'),
        ),
        migrations.AddField(
            model_name='option',
            name='default_text_lang2',
            field=models.TextField(blank=True, default='', help_text='The default text value for the additional input of this option (in the secondary language).', verbose_name='Default text value (secondary)'),
        ),
        migrations.AddField(
            model_name='option',
            name='default_text_lang3',
            field=models.TextField(blank=True, default='', help_text='The default text value for the additional input of this option (in the tertiary language).', verbose_name='Default text value (tertiary)'),
        ),
        migrations.AddField(
            model_name='option',
            name='default_text_lang4',
            field=models.TextField(blank=True, default='', help_text='The default text value for the additional input of this option (in the quaternary language).', verbose_name='Default text value (quaternary)'),
        ),
        migrations.AddField(
            model_name='option',
            name='default_text_lang5',
            field=models.TextField(blank=True, default='', help_text='The default text value for the additional input of this option (in the quinary language).', verbose_name='Default text value (quinary)'),
        ),
    ]
