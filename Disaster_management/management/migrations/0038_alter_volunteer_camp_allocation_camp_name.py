# Generated by Django 5.0.7 on 2024-08-21 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0037_alter_public_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer_camp_allocation',
            name='camp_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.camp'),
        ),
    ]
