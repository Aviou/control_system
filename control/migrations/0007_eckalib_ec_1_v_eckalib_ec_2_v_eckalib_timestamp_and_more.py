# Generated by Django 4.2.4 on 2023-11-30 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0006_eckalib'),
    ]

    operations = [
        migrations.AddField(
            model_name='eckalib',
            name='ec_1_v',
            field=models.FloatField(default=2.33),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eckalib',
            name='ec_2_v',
            field=models.FloatField(default=1.48),
            preserve_default=False,
        ),
        
        migrations.AddField(
            model_name='phkalib',
            name='ph_4_v',
            field=models.FloatField(default=3.8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phkalib',
            name='ph_7_v',
            field=models.FloatField(default=3.4),
            preserve_default=False,
        ),
        
    ]
