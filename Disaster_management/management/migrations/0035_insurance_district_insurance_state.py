# Generated by Django 5.0.7 on 2024-08-13 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0034_remove_camp_alternate_phone_camp_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='district',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='insurance',
            name='state',
            field=models.CharField(default='Not Specified', max_length=100),
        ),
    ]
