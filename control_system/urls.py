"""
URL configuration for control_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ec_control/urls.py
from django.contrib import admin
from django.urls import path
from control import views, tasks 


urlpatterns = [
    path('', views.index, name='index'),
    path('process-ph/', views.process_data_ph, name='process_data_ph'),
    path('process-ec/', views.process_data_ec, name='process_data_ec'),
    path('process-ratio/', views.process_data_ratio, name='process_data_ratio'),
    path('process-wt/', views.process_data_wt, name='process_data_wt'),
    path('admin/', admin.site.urls),
    path('sensor-data-view/', views.sensor_data_view, name='sensor_data_view'),
    path('adjust-wt/', tasks.adjust_wt, name='adjust_wt'),
    path('adjust-ph/', tasks.adjust_ph, name='adjust_ph'),
    path('adjust-ec/', tasks.adjust_ec, name='adjust_ec'),
    path('process-temp/', views.process_data_temp, name='process_data_temp'),
    path('adjust-fan-speed/', tasks.adjust_fan_speed, name='adjust_fan_speed'),
    path('adjust-humid/', tasks.adjust_humid, name='adjust_humid'),
    path('water_plants_task/', tasks.water_plants_task, name='water_plants_task'),
    path('water_plants/', views.water_plants, name='water_plants'),
    path('latest-sensor-data/', views.latest_sensor_data, name='latest_sensor_data'),
    path('save-ph-calibration/', views.save_ph_calibration, name='save_ph_calibration'),
    path('save-ec-calibration/', views.save_ec_calibration, name='save_ec_calibration'),
    path('kali', views.kali, name='kali'),
    path('latest-kalib-data', views.latest_kalib_data, name='latest_kalib_data'),
    path('sensor-data-range/', views.sensor_data_range, name='sensor_data_range'),
    path('grenzwerte', views.grenzwerte, name='grenzwerte'),
    path('latest-grenzwerte-data', views.latest_grenzwerte_data, name='latest_grenzwerte_data'),
    path('submit-ec-grenze', views.submit_ec_grenze, name='submit_ec_grenze'),
    path('submit-ph-grenze', views.submit_ph_grenze, name='submit_ph_grenze'),
    path('submit-wt-grenze', views.submit_wt_grenze, name='submit_wt_grenze'),
    path('submit-humd-grenze', views.submit_humd_grenze, name='submit_humd_grenze'),
    path('submit-temp-grenze', views.submit_temp_grenze, name='submit_temp_grenze'),
    path('submit-wt-grenze', views.submit_wt_grenze, name='submit_wt_grenze'),
    path('submit-gas-grenze', views.submit_gas_grenze, name='submit_gas_grenze'),
    path('submit-waterflow-grenze', views.submit_waterflow_grenze, name='submit_waterflow_grenze'),
    path('send-relay-command/', views.send_relay_command, name='send_relay_command'),
    path('timer/', views.timer, name='timer'), 
    path('get-current-times/', views.get_current_times, name='get_current_times'),
    path('water_volume/', views.water_volume_view, name='water_volume'),

]

