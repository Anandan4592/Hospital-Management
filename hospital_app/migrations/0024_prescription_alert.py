# Generated by Django 5.1.3 on 2024-12-01 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0023_userprofile_soft_deletion'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='alert',
            field=models.BooleanField(default=False),
        ),
    ]