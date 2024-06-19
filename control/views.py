from django.shortcuts import render, redirect
from django.http import JsonResponse,  HttpResponseRedirect
from .models import SensorData, TargetWt, TargetRatio, TargetHumid, TargetEc, Relay, TargetPh, CalculatedValues, WaterVolume, SensorSoilMoisture, WaterLevelHumid, SensorData2, CalibrationEc, SensorMoisture, CalibrationPh, GrenzwerteWaterflow, GrenzwerterSensorGas, GrenzwerteSensorEc, GrenzwerteSensorPh, GrenzwerteSensorHumd, TargetTemp, GrenzwerteSensorTemp, GrenzwerteSensorWt, SensorDataOutdoor, CurrentPhase
import json
import logging
from celery import shared_task
from .tasks import adjust_ph, adjust_ec, adjust_wt, adjust_fan_speed, adjust_humid, water_plants_task
from .calc import berechne_ph_wert, berechne_ec
from django.views.decorators.csrf import csrf_exempt
from .forms import MoistureForm
from django.urls import reverse
from .mqtt_client import client
from django.utils import timezone
from datetime import timedelta


# Logger-Konfiguration
logger = logging.getLogger(__name__)

def index(request):
    latest_raw_data = SensorData.objects.order_by('-id').first()
    latest_data = CalculatedValues.objects.order_by('-id').first()
    target_ec = TargetEc.objects.order_by('-id').first() or {}
    target_ph = TargetPh.objects.order_by('-id').first() or {}
    target_ratio = TargetRatio.objects.order_by('-id').first() or {}
    target_wt = TargetWt.objects.order_by('-id').first() or {}
    target_temp = TargetTemp.objects.order_by('-id').first() or {}
    latest_data2 = SensorData2.objects.order_by('-id').first()
    latest_data_water_level = WaterLevelHumid.objects.order_by('-id').first()
    latest_data_outdoor = SensorDataOutdoor.objects.order_by('-id').first()
    latest_data_water_tank = WaterVolume.objects.order_by('-id').first()
    return render(request, 'index.html', {
        'latest_raw_data': latest_raw_data,
        'latest_data': latest_data,
        'target_ec': target_ec,
        'target_ph': target_ph,
        'target_ratio': target_ratio,
        'target_wt': target_wt,
        'latest_data2': latest_data2,
        'latest_data_outdoor': latest_data_outdoor,
        'target_temp': target_temp,
        'latest_data_water_level': latest_data_water_level,
        'latest_data_water_tank': latest_data_water_tank,
    })

def kali(request): 
    latest_ph_cali = CalibrationPh.objects.last()
    latest_ec_cali = CalibrationEc.objects.last()
    return render(request,'kali.html',{
        'latest_ph_cali': latest_ph_cali,
        'latest_ec_cali': latest_ec_cali,
        
    })

def latest_kalib_data(request):
    latest_ph_cali = CalibrationPh.objects.latest('timestamp')
    latest_ec_cali = CalibrationEc.objects.latest('timestamp')
    context = {
        'data': {
            'ph4': latest_ph_cali.ph4,
            'ph7': latest_ph_cali.ph7,
            'ph9': latest_ph_cali.ph9,
            'ec1': latest_ec_cali.ec1,
            'ec5': latest_ec_cali.ec5,
            'ec12': latest_ec_cali.ec12,
        }
    }
    return render(request, 'kali.html', context)

def grenzwerte(request):
    sensor_data = CalculatedValues.objects.last()
    sensor2_data = SensorData2.objects.last()
    latest_grenzwerte_ph = GrenzwerteSensorPh.objects.last()
    latest_grenzwerte_ec = GrenzwerteSensorEc.objects.last()
    latest_grenzwerte_temp = GrenzwerteSensorTemp.objects.last()
    latest_grenzwerte_humd = GrenzwerteSensorHumd.objects.last()
    latest_grenzwerte_wt = GrenzwerteSensorWt.objects.last()
    latest_grenzwerte_gas = GrenzwerterSensorGas.objects.last()
    latest_grenzwerte_waterflow = GrenzwerteWaterflow.objects.last()
    return render(request, 'grenzwerte.html', {
        'latest_grenzwerte_ph': latest_grenzwerte_ph,
        'latest_grenzwerte_ec': latest_grenzwerte_ec,
        'latest_grenzwerte_temp': latest_grenzwerte_temp,
        'latest_grenzwerte_humd': latest_grenzwerte_humd,
        'latest_grenzwerte_wt': latest_grenzwerte_wt,
        'latest_grenzwerte_gas': latest_grenzwerte_gas,
        'latest_grenzwerte_waterflow': latest_grenzwerte_waterflow,
        'sensor_data': sensor_data,
        'sensor2_data': sensor2_data,
    })

def latest_grenzwerte_data(request):
    sensor_data = CalculatedValues.objects.last('timestamp')
    sensor2_data = SensorData2.objects.last('timestamp')
    latest_grenzwerte_ph = GrenzwerteSensorPh.objects.last('timestamp')
    latest_grenzwerte_ec = GrenzwerteSensorEc.objects.last('timestamp')
    latest_grenzwerte_temp = GrenzwerteSensorTemp.objects.last('timestamp')
    latest_grenzwerte_humd = GrenzwerteSensorHumd.objects.last('timestamp')
    latest_grenzwerte_wt = GrenzwerteSensorWt.objects.last('timestamp')
    latest_grenzwerte_gas = GrenzwerterSensorGas.objects.last('timestamp')
    latest_grenzwerte_waterflow = GrenzwerteWaterflow.objects.last('timestamp')
    context = {
        'data': {
            'ph': sensor_data.ph,
            'ec': sensor_data.ec,
            'water_temp': sensor_data.water_temp,
            'temperature1': sensor2_data.temperature1,
            'temperature2': sensor2_data.temperature2,
            'humidity1': sensor2_data.humidity1,
            'humidity2': sensor2_data.humidity2,
            'waterTemp1': sensor2_data.waterTemp1,
            'waterTemp2': sensor2_data.waterTemp2,
            'water_level': sensor2_data.water_level,
            'ph_min': latest_grenzwerte_ph.ph_min,
            'ph_max': latest_grenzwerte_ph.ph_max,
            'ec_min': latest_grenzwerte_ec.ec_min,
            'ec_max': latest_grenzwerte_ec.ec_max,
            'temp_min': latest_grenzwerte_temp.temp_min,
            'temp_max': latest_grenzwerte_temp.temp_max,
            'humd_min': latest_grenzwerte_humd.humd_min,
            'humd_max': latest_grenzwerte_humd.humd_max,
            'temp_wt_min': latest_grenzwerte_wt.temp_wt_min,
            'temp_wt_max': latest_grenzwerte_wt.temp_wt_max,
            'gas_grenzwert': latest_grenzwerte_gas.gas_grenzwert,
            'waterflow_grenzwert': latest_grenzwerte_waterflow.waterflow_grenzwert,

        }
    }
    return render(request, 'grenzwerte.html', context)

def submit_ec_grenze(request):
    if request.method == "POST":
        GrenzwerteSensorEc.objects.create(
            ec_min=request.POST.get('ec_min'),
            ec_max=request.POST.get('ec_max'),
        )
    return HttpResponseRedirect(reverse('grenzwerte'))   

def submit_ph_grenze(request):
    if request.method == "POST":
        GrenzwerteSensorPh.objects.create(
            ph_min=request.POST.get('ph_min'),
            ph_max=request.POST.get('ph_max'),
        )
    return HttpResponseRedirect(reverse('grenzwerte'))   

def submit_temp_grenze(request):
    if request.method == "POST":
        GrenzwerteSensorTemp.objects.create(
            temp_min=request.POST.get('temp_min'),
            temp_max=request.POST.get('temp_max'),
        )
    return HttpResponseRedirect(reverse('grenzwerte'))   
    
def submit_humd_grenze(request):
    if request.method == "POST":
        GrenzwerteSensorHumd.objects.create(
            humd_min=request.POST.get('humd_min'),
            humd_max=request.POST.get('humd_max'),
        )
    return HttpResponseRedirect(reverse('grenzwerte'))   

def submit_wt_grenze(request):
    if request.method == "POST":
        GrenzwerteSensorWt.objects.create(
            temp_wt_min=request.POST.get('temp_wt_min'),
            temp_wt_max=request.POST.get('temp_wt_max'),
        )
    return HttpResponseRedirect(reverse('grenzwerte'))   

def submit_gas_grenze(request):
    if request.method == "POST":
        GrenzwerterSensorGas.objects.create(
            gas_grenzwert=request.POST.get('gas_grenzwert'),
        )
    return HttpResponseRedirect(reverse('grenzwerte'))

def submit_waterflow_grenze(request):
    if request.method == "POST":
        GrenzwerteWaterflow.objects.create(
            waterflow_grenzwert=request.POST.get('waterflow_grenzwert'),
        )
    return HttpResponseRedirect(reverse('grenzwerte'))

def save_ph_calibration(request):
    if request.method == "POST":
        CalibrationPh.objects.create(
            ph4=request.POST.get('ph4'),
            ph7=request.POST.get('ph7'),
            ph9=request.POST.get('ph9'),
        )
    return HttpResponseRedirect(reverse('kali'))  
    
def save_ec_calibration(request):
    if request.method == "POST":
         CalibrationEc.objects.create(
            ec1=request.POST.get('ec1'),
            ec5=request.POST.get('ec5'),
            ec12=request.POST.get('ec12'),
        )
    return HttpResponseRedirect(reverse('kali'))  # Leite zurück zur Hauptseite


@csrf_exempt
def sensor_data_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Empfangene Daten: {data}")
            
            # Verarbeitung für allgemeine Sensordaten
            if 'raw_ph_voltage' in data and 'raw_ec_voltage' in data and 'temperature' in data:
                raw_ph_voltage = data['raw_ph_voltage']
                raw_ec_voltage = data['raw_ec_voltage']
                temperature = data['temperature']

                SensorData.objects.create(
                    raw_ph_voltage=raw_ph_voltage,
                    raw_ec_voltage=raw_ec_voltage,
                    temperature=temperature
                )
    
                ph = berechne_ph_wert(raw_ph_voltage, temperature)
                ec = berechne_ec(raw_ec_voltage, temperature)

                CalculatedValues.objects.create(ph=ph, ec=ec, water_temp=temperature)

                return JsonResponse({'status': 'success', 'ph': ph, 'ec': ec})

            # Spezifische Verarbeitung für SensorData2
            elif set(['humidity1', 'temperature1', 'humidity2', 'temperature2', 'pressure1', 'pressure2', 'waterTemp1', 'waterTemp2', 'distance', 'flowRate']).issubset(data.keys()):
                SensorData2.objects.create(
                    temperature1=round(float(data.get('temperature1', 0)), 2),
                    humidity1=round(float(data.get('humidity1', 0)), 2),
                    temperature2=round(float(data.get('temperature2', 0)), 2),
                    humidity2=round(float(data.get('humidity2', 0)), 2), 
                    pressure1=round(float(data.get('pressure1', 0)), 2),
                    pressure2=round(float(data.get('pressure2', 0)), 2),
                    waterTemp1=round(float(data.get('waterTemp1', 0)), 2),
                    waterTemp2=round(float(data.get('waterTemp2', 0)), 2),
                    distance = float(data.get('distance', 0)),
                    flowRate =float(data.get('flowRate', 0)),  # Verwende 'N/A' als Standardwert
                   
                )
                logger.info("SensorData2 Daten erfolgreich gespeichert.")
                return JsonResponse({'status': 'success', 'message': 'SensorData2 Daten erfolgreich gespeichert.'})
            
            elif set(['soilMoisture1', 'soilMoisture2']).issubset(data.keys()):
                SensorSoilMoisture.objects.create(
                    soilMoisture1 = float(data.get('soilMoisture1', 0)),
                    soilMoisture2 = float(data.get('soilMoisture2', 0)),
                )
                logger.info("SensorMoisture Daten erfolgreich gespeichert.")
                return JsonResponse({'status': 'success', 'message': 'SensorMoisture Daten erfolgreich gespeichert.'})
            
            
            elif set(['temperature01', 'humidity01', 'temperature02', 'humidity02', 'temperature03', 'humidity03', 'soil_temp01', 'soil_temp02', 'soil_temp03']).issubset(data.keys()):
                SensorDataOutdoor.objects.create(
                    temperature01=round(float(data.get('temperature01', 0)), 2),
                    humidity01=round(float(data.get('humidity01', 0)), 2),
                    temperature02=round(float(data.get('temperature02', 0)), 2),
                    humidity02=round(float(data.get('humidity02', 0)), 2), 
                    temperature03=round(float(data.get('temperature03', 0)), 2),
                    humidity03=round(float(data.get('humidity03', 0)), 2),
                    soil_temp01=round(float(data.get('soil_temp01', 0)), 2),
                    soil_temp02=round(float(data.get('soil_temp02', 0)), 2),
                    soil_temp03=round(float(data.get('soil_temp03', 0)), 2),
                )
                logger.info("SensorDataOutdoor Daten erfolgreich gespeichert.")
                return JsonResponse({'status': 'success', 'message': 'SensorDataOutdoor Daten erfolgreich gespeichert.'})
            
            elif set(['moisture01', 'moisture02', 'moisture03']).issubset(data.keys()):
                SensorMoisture.objects.create(
                    moisture01=round(float(data.get('moisture01', 0)), 2),
                    moisture02=round(float(data.get('moisture02', 0)), 2),
                    moisture03=round(float(data.get('moisture03', 0)), 2),
                )
                logger.info("SensorMoisture Daten erfolgreich gespeichert.")
                return JsonResponse({'status': 'success', 'message': 'SensorDataOutdoor Daten erfolgreich gespeichert.'})
            
            elif set(['moisture01', 'moisture02', 'moisture03']).issubset(data.keys()):
                WaterLevelHumid.objects.create(
                    water_level=data.get('water_level', 'N/A')
                )
                logger.info("SensorMoisture Daten erfolgreich gespeichert.")
                return JsonResponse({'status': 'success', 'message': 'SensorDataOutdoor Daten erfolgreich gespeichert.'})
            else:
                logger.error("Unbekanntes Datenformat.")
                return JsonResponse({'error': 'Unbekanntes Datenformat'}, status=400)
             
            
        except json.JSONDecodeError as e:
            logger.error(f"Fehler beim Parsen der Daten: {e}")
            return JsonResponse({'error': 'Fehler beim Parsen der Daten'}, status=400)
        except Exception as e:
            logger.error(f"Fehler bei der Anfrageverarbeitung: {e}")
            return JsonResponse({'error': 'Fehler bei der Anfrageverarbeitung'}, status=500)

    else:
        return JsonResponse({'error': 'Diese Endpoint unterstützt nur POST-Anfragen.'}, status=405)

def latest_sensor_data(request):
    latest_data = CalculatedValues.objects.order_by('-id').first()
    latest_data2 = SensorData2.objects.order_by('-id').first()
    latest_raw_data = SensorData.objects.order_by('-id').first()
    latest_data_outdoor = SensorDataOutdoor.objects.order_by('-id').first()
    latest_data_moisture = SensorMoisture.objects.order_by('-id').first()
    latest_data_water_level = WaterLevelHumid.objects.order_by('-id').first()
    latest_data_water_tank = WaterVolume.objects.order_by('-id').first()
    latest_sensor_moisture = SensorSoilMoisture.objects.order_by('-id').first()
    latest_target_humid = TargetHumid.objects.order_by('-id').first()

    response_data = {
        'ph': latest_data.ph if latest_data else 'N/A',
        'ec': latest_data.ec if latest_data else 'N/A',
        'timestamp': latest_data.timestamp if latest_data else 'N/A',
        'water_temp': latest_data.water_temp if latest_data else 'N/A',
        'temperature1': latest_data2.temperature1 if latest_data2 else 'N/A',
        'temperature2': latest_data2.temperature2 if latest_data2 else 'N/A',
        'humidity1': latest_data2.humidity1 if latest_data2 else 'N/A',
        'humidity2': latest_data2.humidity2 if latest_data2 else 'N/A',
        'pressure1': latest_data2.pressure1 if latest_data2 else 'N/A',
        'pressure2': latest_data2.pressure2 if latest_data2 else 'N/A',
        'waterTemp1': latest_data2.waterTemp1 if latest_data2 else 'N/A',
        'waterTemp2': latest_data2.waterTemp2 if latest_data2 else 'N/A',
        'distance': latest_data2.distance if latest_data2 else 'N/A',
        'soilMoisture1': latest_sensor_moisture.soilMoisture1 if latest_sensor_moisture else 'N/A',
        'soilMoisture2': latest_sensor_moisture.soilMoisture2 if latest_sensor_moisture else 'N/A',
        'volume': latest_data_water_tank.volume if latest_data_water_tank else 'N/A',
        'water_level': latest_data_water_level.water_level if latest_data_water_level else 'N/A',
        'ph_voltage': latest_raw_data.raw_ph_voltage if latest_raw_data else 'N/A',
        'ec_voltage': latest_raw_data.raw_ec_voltage if latest_raw_data else 'N/A',
        'flowRate': latest_data2.flowRate if latest_data2 else 'N/A',
        'temperature01': latest_data_outdoor.temperature01 if latest_data_outdoor else 'N/A',
        'humidity01': latest_data_outdoor.humidity01 if latest_data_outdoor else 'N/A',
        'temperature02': latest_data_outdoor.temperature02 if latest_data_outdoor else 'N/A',
        'humidity02': latest_data_outdoor.humidity02 if latest_data_outdoor else 'N/A',
        'temperature03': latest_data_outdoor.temperature03 if latest_data_outdoor else 'N/A',
        'humidity03': latest_data_outdoor.humidity03 if latest_data_outdoor else 'N/A',
        'moisture01': latest_data_moisture.moisture01 if latest_data_moisture else 'N/A',
        'moisture02': latest_data_moisture.moisture02 if latest_data_moisture else 'N/A',
        'moisture03': latest_data_moisture.moisture03 if latest_data_moisture else 'N/A',
        'soil_temp01': latest_data_outdoor.soil_temp01 if latest_data_outdoor else 'N/A',
        'soil_temp02': latest_data_outdoor.soil_temp02 if latest_data_outdoor else 'N/A',
        'soil_temp03': latest_data_outdoor.soil_temp03 if latest_data_outdoor else 'N/A',
        'target_humidity': latest_target_humid.target_humidity if latest_target_humid else 'N/A',
    }
    return JsonResponse(response_data)


@shared_task           
def process_data_ec(request):
    if request.method == 'POST':
        print(request.POST) 
        try:
            target_ec = float(request.POST.get('target_ec'))
            

            TargetEc.objects.create(
                target_ec=target_ec,
            )

           
        except ValueError as e:
            logger.error(f"Fehler bei der Eingabevalidierung: {e}")
            return JsonResponse({'error': 'Invalid input'}, status=400)
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung: {e}")
            return JsonResponse({'error': 'Error processing request'}, status=500)

        return redirect('index')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@shared_task
def process_data_ph(request):
    if request.method == 'POST':
        print(request.POST) 
        try:
            # Zielwerte aus dem Formular abrufen und validieren
            target_ph = float(request.POST.get('target_ph'))
            pump_time_ph = float(request.POST.get('pump_time_ph'))

            TargetPh.objects.create(
                target_ph=target_ph,
                pump_time_ph=pump_time_ph
            )

            adjust_ph()

        except ValueError as e:
            logger.error(f"Fehler bei der Eingabevalidierung: {e}")
            return JsonResponse({'error': 'Invalid input'}, status=400)
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung: {e}")
            return JsonResponse({'error': 'Error processing request'}, status=500)

        return redirect('index')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
@shared_task
def process_data_wt(request):
    if request.method == 'POST':
        print(request.POST) 
        try:
            target_water_temp = float(request.POST.get('target_water_temp'))
            
            # Zielwerte in der Datenbank speichern
            TargetWt.objects.create(  
                target_water_temp=target_water_temp,
            )
    
            adjust_wt()

        except ValueError as e:
            logger.error(f"Fehler bei der Eingabevalidierung: {e}")
            return JsonResponse({'error': 'Invalid input'}, status=400)
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung: {e}")
            return JsonResponse({'error': 'Error processing request'}, status=500)

        return redirect('index')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@shared_task
def process_data_ratio(request):
    if request.method == 'POST':
        print(request.POST) 
        try:
            n_ratio = float(request.POST.get('n_ratio'))
            p_ratio = float(request.POST.get('p_ratio'))
            k_ratio = float(request.POST.get('k_ratio'))
            pump_time_ratio = float(request.POST.get('pump_time_ratio'))
            # Zielwerte in der Datenbank speichern
            TargetRatio.objects.create(
                n_ratio=n_ratio,
                p_ratio=p_ratio,
                k_ratio=k_ratio,
                pump_time_ratio=pump_time_ratio
            )
    
            adjust_ec()

        except ValueError as e:
            logger.error(f"Fehler bei der Eingabevalidierung: {e}")
            return JsonResponse({'error': 'Invalid input'}, status=400)
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung: {e}")
            return JsonResponse({'error': 'Error processing request'}, status=500)

        return redirect('index')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@shared_task
def process_data_temp(request):
    if request.method == 'POST':
        print(request.POST) 
        try:
            target_temperature = float(request.POST.get('target_temperature'))
            
            TargetTemp.objects.create(
                target_temperature=target_temperature,
            )
    
            adjust_fan_speed()

        except ValueError as e:
            logger.error(f"Fehler bei der Eingabevalidierung: {e}")
            return JsonResponse({'error': 'Invalid input'}, status=400)
        except Exception as e:
            logger.error(f"Fehler bei der Verarbeitung: {e}")
            return JsonResponse({'error': 'Error processing request'}, status=500)

        return redirect('index')
    

def sensor_data_range(request):
    # Beispiel für Parameter: 'time_span' kann 'day', 'week', 'month', 'year' sein
    time_span = request.GET.get('time_span', 'day')

    # Die aktuelle Zeit für das Filtern der Daten
    now = timezone.now()

    if time_span == 'day':
        start_date = now - timedelta(days=1)
    elif time_span == 'week':
        start_date = now - timedelta(weeks=1)
    elif time_span == 'month':
        start_date = now - timedelta(days=30) # Oder die genaue Anzahl von Tagen im letzten Monat
    elif time_span == 'year':
        start_date = now - timedelta(days=365)
    else:
        # Standardwert, falls 'time_span' nicht erkannt wird
        start_date = now - timedelta(days=1)

    # Filtern der Daten
    data = CalculatedValues.objects.filter(timestamp__gte=start_date)
    data1 = SensorData2.objects.filter(timestamp__gte=start_date)
    # Konvertierung der Daten in ein JSON-Format
    data_list = list(data.values('ph', 'ec', 'water_temp', 'timestamp'))
    data_list1 = list(data1.values('temperature1', 'temperature2', 'humidity1', 'humidity2', 'waterTemp1', 'waterTemp2', 'timestamp'))
    # Senden der Daten als JSON-Antwort
    return JsonResponse({'data': data_list,'data1': data_list1})

def timer(request):
    return render(request, 'timer.html')

@csrf_exempt
def get_current_times(request):
    if request.method == 'GET':
        relay_name = request.GET.get('relay')
        relay = Relay.objects.get(name=relay_name)
        return JsonResponse({
            'runTime': relay.run_time,
            'pauseTime': relay.pause_time
        })
    

@csrf_exempt
def send_relay_command(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        relay_name = data['relay']
        stop_command = data.get('stop', False)

    if stop_command:
        message1 = "stop"
        client.publish(f"str/{relay_name}", message1)
    else:
        runTime = int(data['runTime']) * 60  # Minuten in Sekunden umrechnen
        pauseTime = int(data['pauseTime']) * 60  # Minuten in Sekunden umrechnen
        message = f"{runTime},{pauseTime}"

        relay, created = Relay.objects.get_or_create(name=relay_name)
        relay.run_time = runTime
        relay.pause_time = pauseTime
        relay.save()

        message = f"{runTime},{pauseTime}"
        topic = f"str/{relay}"
        
    
        client.publish(topic, message)
       
        
        return JsonResponse({'status': 'success', 'message': 'Command sent'})
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)


def water_volume_view(request):
    latest_volume = WaterVolume.objects.last()
    return render(request, 'index.html', {'latest_volume': latest_volume})



def water_plants(request):
    task_id = None
    # Hole oder erstelle die aktuelle Phase
    current_phase = CurrentPhase.objects.first() or CurrentPhase.objects.create()
    
    if request.method == 'POST':
        form = MoistureForm(request.POST)
        if form.is_valid():
            phase = form.cleaned_data['phase']
            current_phase.phase = phase
            current_phase.save()
            result = water_plants_task.delay()
            task_id = result.id
            return redirect('water_plants')  # Umleiten, um ein erneutes Absenden des Formulars zu verhindern
    else:
        form = MoistureForm(initial={'phase': current_phase.phase})

    return render(request, 'index.html', {'form': form, 'task_id': task_id, 'current_phase': current_phase})
