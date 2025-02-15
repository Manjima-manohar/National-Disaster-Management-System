# Generated by Django 5.0.7 on 2024-07-17 09:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person_missing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('dob', models.DateField()),
                ('blood_group', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=100)),
                ('occupation', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=30)),
                ('mother_name', models.CharField(max_length=30)),
                ('photo', models.ImageField(upload_to='media/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_missing_entries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
