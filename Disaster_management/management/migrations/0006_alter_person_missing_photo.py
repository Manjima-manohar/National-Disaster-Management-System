# Generated by Django 5.0.7 on 2024-07-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_person_missing_address_person_missing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person_missing',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
