# Generated by Django 5.0.7 on 2024-08-21 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0038_alter_volunteer_camp_allocation_camp_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camp',
            name='camp_name',
            field=models.CharField(max_length=100),
        ),
    ]
