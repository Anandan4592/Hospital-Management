# Generated by Django 5.1.3 on 2024-11-29 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0018_bedallocation_medical_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='discharge',
            name='bill_payed',
            field=models.BooleanField(default=False),
        ),
    ]
