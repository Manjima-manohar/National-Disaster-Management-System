# Generated by Django 5.0.7 on 2024-08-13 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0032_vehicle_management_district_vehicle_management_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer_camp_allocation',
            name='state',
            field=models.CharField(default='Not Specified', max_length=100),
        ),
    ]
