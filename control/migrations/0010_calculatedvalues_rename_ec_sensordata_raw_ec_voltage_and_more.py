# Generated by Django 5.0.1 on 2024-03-10 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0009_rename_ec_1_v_vokalib_ec_v_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculatedValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph', models.FloatField()),
                ('ec', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='sensordata',
            old_name='ec',
            new_name='raw_ec_voltage',
        ),
        migrations.RenameField(
            model_name='sensordata',
            old_name='ph',
            new_name='raw_ph_voltage',
        ),
        migrations.RenameField(
            model_name='sensordata',
            old_name='water_temp',
            new_name='temperature',
        ),
    ]
