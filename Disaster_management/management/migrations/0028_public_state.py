# Generated by Django 5.0.7 on 2024-08-12 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0027_remove_volunteer_camp_allocation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='public',
            name='state',
            field=models.CharField(default='Not Specified', max_length=100),
        ),
    ]
