from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0064_integration_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='read_only',
            field=models.BooleanField(
                default=False,
                help_text='Designates whether this value can be changed by users.',
                verbose_name='Read only',
            ),
        ),
    ]
