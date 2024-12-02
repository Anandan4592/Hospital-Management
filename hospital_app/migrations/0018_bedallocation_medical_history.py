# Generated by Django 5.1.3 on 2024-11-29 16:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0017_discharge'),
    ]

    operations = [
        migrations.AddField(
            model_name='bedallocation',
            name='medical_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital_app.medicalhistory'),
        ),
    ]