# Generated by Django 5.0.7 on 2024-07-23 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_person_missing_camp_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Police_station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policestation_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('district', models.CharField(max_length=100)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='policestation_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
