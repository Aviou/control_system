from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_system.settings')

app = Celery('control')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'adjust_ph_every_10_minutes': {
        'task': 'control.tasks.adjust_ph',
        'schedule': crontab(minute='*/20'),
    },

    'adjust_ec_every_10_minutes': {
        'task': 'control.tasks.adjust_ec',
        'schedule': crontab(minute='*/10'),
    },

    'adjust_wt_every_10_minutes': {
        'task': 'control.tasks.adjust_wt',
        'schedule': crontab(minute='*/10'),
    },

    'adjust_fan_speed':{
        'task': 'control.tasks.adjust_fan_speed',
        'schedule': crontab(minute= '*/5'),
    },

    'adjust_humid':{
        'task': 'control.tasks.adjust_humid',
        'schedule': crontab(minute= '*/10'),
    },

    'save-water-volume-every-minute': {
        'task': 'control.tasks.save_water_volume',
        'schedule': crontab(minute='*/1'),
    },

    'water_plants_task': {
        'task': 'control.tasks.water_plants_task',
        'schedule': crontab(minute='*/15'),
    },
}
# Automatische Task-Entdeckung
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

