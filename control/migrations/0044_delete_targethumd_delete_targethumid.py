# Generated by Django 5.0.1 on 2024-06-08 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0043_remove_sensordata2_soil_moisture1_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TargetHumd',
        ),
        migrations.DeleteModel(
            name='TargetHumid',
        ),
    ]