# Generated by Django 5.0.1 on 2024-05-30 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0033_targethumid'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterLevelHumid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_level', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaterVolume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('volume', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='sensordata2',
            name='water_level',
        ),
        migrations.AddField(
            model_name='sensordata2',
            name='distance',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
