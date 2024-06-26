# Generated by Django 5.0.1 on 2024-03-31 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0018_targetvalues_timestamp_alter_targetvalues_k_ratio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TargetEc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_ec', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TargetPh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_ph', models.FloatField()),
                ('pump_time_ph', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TargetRatio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_ratio', models.FloatField()),
                ('p_ratio', models.FloatField()),
                ('k_ratio', models.FloatField()),
                ('pump_time_ratio', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TargetWt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_water_temp', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='TargetValues',
        ),
    ]
