# Generated by Django 5.0.7 on 2024-07-22 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_alter_person_missing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person_missing',
            name='status',
            field=models.CharField(choices=[('Searching', 'SEARCHING'), ('founded', 'FOUNDED')], default='Searching', max_length=100),
        ),
    ]
