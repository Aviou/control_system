# Generated by Django 5.0.1 on 2024-03-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0010_calculatedvalues_rename_ec_sensordata_raw_ec_voltage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculatedvalues',
            name='water_temp',
            field=models.FloatField(default=22),
            preserve_default=False,
        ),
    ]