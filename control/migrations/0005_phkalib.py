# Generated by Django 4.2.6 on 2023-11-28 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0004_rename_water_temperature_sensordata_water_temp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhKalib',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph_7', models.FloatField()),
                ('ph_4', models.FloatField()),
            ],
        ),
    ]
