# Generated by Django 5.0.7 on 2024-08-13 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0033_volunteer_camp_allocation_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camp',
            name='alternate_phone',
        ),
        migrations.AddField(
            model_name='camp',
            name='state',
            field=models.CharField(default='Not Specified', max_length=100),
        ),
    ]
