# Generated by Django 5.1.3 on 2024-11-30 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0021_medicalhistory_lab_report_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalhistory',
            name='is_inpatient',
            field=models.BooleanField(default=False),
        ),
    ]
