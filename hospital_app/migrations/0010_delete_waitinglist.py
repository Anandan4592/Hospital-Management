# Generated by Django 5.1.3 on 2024-11-28 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0009_medicalhistory_appointment_medicalhistory_doctor_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WaitingList',
        ),
    ]
