# Generated by Django 5.1.3 on 2024-11-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0011_roomtype_bedallocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtype',
            name='room_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
