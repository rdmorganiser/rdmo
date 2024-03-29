# Generated by Django 2.2.18 on 2021-04-20 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0026_optionset_option_locked'),
        ('questions', '0057_question_default_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='default_option',
            field=models.ForeignKey(blank=True, help_text='The default option for this question. To be used with regular optionsets.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='options.Option', verbose_name='Default option'),
        ),
    ]
