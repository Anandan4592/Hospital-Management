# Generated by Django 5.1.3 on 2024-11-30 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0020_alter_discharge_discharge_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalhistory',
            name='lab_report_cost',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
