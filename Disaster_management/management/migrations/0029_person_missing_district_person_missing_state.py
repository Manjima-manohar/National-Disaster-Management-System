# Generated by Django 5.0.7 on 2024-08-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0028_public_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='person_missing',
            name='district',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='person_missing',
            name='state',
            field=models.CharField(default='Not Specified', max_length=100),
        ),
    ]
