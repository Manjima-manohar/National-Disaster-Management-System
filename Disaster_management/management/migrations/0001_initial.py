# Generated by Django 5.0.7 on 2024-07-17 08:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camp_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('place', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('district', models.CharField(max_length=100)),
                ('camp_head', models.CharField(default='', max_length=30)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='camp_allocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('blood_group', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=100)),
                ('occupation', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=30)),
                ('mother_name', models.CharField(max_length=30)),
                ('district', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='media/')),
                ('camp_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.camp')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='public_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
