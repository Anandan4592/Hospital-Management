# Generated by Django 5.1.3 on 2024-12-02 04:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0028_discharge_insurance_applied'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_company', models.CharField(blank=True, max_length=20, null=True)),
                ('insurance_number', models.CharField(blank=True, max_length=20, null=True)),
                ('applied_date', models.DateTimeField(auto_now_add=True)),
                ('discharge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_app.discharge')),
            ],
        ),
    ]