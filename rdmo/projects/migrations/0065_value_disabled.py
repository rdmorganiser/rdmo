from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0064_integration_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='disabled',
            field=models.BooleanField(
                default=False,
                help_text='Designates whether this value is disabled for editing by users.',
                verbose_name='Disabled',
            ),
        ),
    ]
