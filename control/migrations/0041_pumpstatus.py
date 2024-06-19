# Generated by Django 5.0.1 on 2024-06-07 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0040_currentphase'),
    ]

    operations = [
        migrations.CreateModel(
            name='PumpStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('last_pump_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
