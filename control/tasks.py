from celery import shared_task
from .models import TargetRatio, CalculatedValues, TargetWt, TargetPh, TargetHumid, SensorSoilMoisture, TargetEc, SensorData2, TargetTemp, WaterVolume, CurrentPhase, PumpStatus
from .mqtt_client import client
from celery.utils.log import get_task_logger
from .pid_controller import pid_n, pid_p, pid_k, pid_ph, pid_humid, pid_fan_ultra, pid_fan_humid, pid_fan_speed, pid_wt
from .water_calc import update_remaining_water_volume
from django.conf import settings
from datetime import datetime, timedelta
import math

logger = get_task_logger(__name__)

PHASE_PARAMETERS = settings.PHASE_PARAMETERS


@shared_task
def save_water_volume():
    remaining_volume = update_remaining_water_volume()
    if remaining_volume > 0:
        WaterVolume.objects.create(volume=remaining_volume)
    else:
        print("Fehler: Kein gültiger Wert für remaining_volume")


@shared_task
def adjust_ph():
    tolerance = 0.2
    latest_data = CalculatedValues.objects.last()
    target_values = TargetPh.objects.last()
    latest_volume = WaterVolume.objects.last()
    if latest_data and target_values:
        remaining_water_volume = latest_volume.volume

        # Herstellerempfehlungen in ml/l für pH
        pump_time_ph = target_values.pump_time_ph  # Annahme: Pumpzeit in ml/l

        # Berechne die notwendige Düngermenge in ml basierend auf der verbleibenden Wassermenge
        total_ml_ph = remaining_water_volume * pump_time_ph

        # Berechne die Pumpzeit in Sekunden (Pumpenrate ist 1,25 ml/s)
        pump_time_ph_seconds = total_ml_ph / 1.25  # in Sekunden

        # Konvertiere die Pumpzeit in Millisekunden
        pump_time_ph_ms = pump_time_ph_seconds * 1000

        # Update setpoint for pH
        pid_ph.setpoint = target_values.target_ph

        # Get current pH value and calculate control value
        control_value = pid_ph(latest_data.ph)

        if latest_data.ph < target_values.target_ph - tolerance:
            # Adjust pump time with PID control value
            adjusted_pump_time_ph_ms = pump_time_ph_ms * control_value
            if control_value > 0:
                client.publish("str/php", str(int(adjusted_pump_time_ph_ms)))
        elif latest_data.ph > target_values.target_ph + tolerance:
            # Adjust pump time with PID control value
            adjusted_pump_time_ph_ms = pump_time_ph_ms * control_value
            if control_value < 0:
                client.publish("str/phm", str(abs(int(adjusted_pump_time_ph_ms))))

    return {'status': 'success'}

@shared_task
def adjust_ec():
    tolerance = 0.2
    latest_data = CalculatedValues.objects.last()
    target_values = TargetRatio.objects.last()
    target_ec = TargetEc.objects.last()
    latest_volume = WaterVolume.objects.last()
    if latest_data and target_ec and target_values:
        remaining_water_volume = latest_volume.volume

        # Herstellerempfehlungen in ml/l werden aus target_values genommen
        n_ml_per_l = target_values.n_ratio  # Beispielwert 0.6
        p_ml_per_l = target_values.p_ratio  # Beispielwert 0.6
        k_ml_per_l = target_values.k_ratio  # Beispielwert 0.6

        # Berechne die notwendige Düngermenge in ml basierend auf der verbleibenden Wassermenge
        n_total_ml = remaining_water_volume * n_ml_per_l
        p_total_ml = remaining_water_volume * p_ml_per_l
        k_total_ml = remaining_water_volume * k_ml_per_l

        # Berechne die Pumpzeiten in Sekunden (Pumpenrate ist 1,25 ml/s)
        n_pump_time = n_total_ml / 1.25  # in Sekunden
        p_pump_time = p_total_ml / 1.25  # in Sekunden
        k_pump_time = k_total_ml / 1.25  # in Sekunden

        # Konvertiere die Pumpzeiten in Millisekunden
        n_pump_time_ms = n_pump_time * 1000
        p_pump_time_ms = p_pump_time * 1000
        k_pump_time_ms = k_pump_time * 1000

        # Update setpoints for each nutrient based on target EC ratio
        pid_n.setpoint = target_ec.target_ec * target_values.n_ratio
        pid_p.setpoint = target_ec.target_ec * target_values.p_ratio
        pid_k.setpoint = target_ec.target_ec * target_values.k_ratio

        # Get current EC value and calculate control values
        control_value_n = pid_n(latest_data.ec)
        control_value_p = pid_p(latest_data.ec)
        control_value_k = pid_k(latest_data.ec)

        if latest_data.ec < target_ec.target_ec - tolerance:
            # Adjust pump times with PID control values
            adjusted_n_pump_time_ms = n_pump_time_ms * control_value_n
            adjusted_p_pump_time_ms = p_pump_time_ms * control_value_p
            adjusted_k_pump_time_ms = k_pump_time_ms * control_value_k

            # Publish pump times to MQTT in milliseconds
            client.publish("str/n_pump", str(int(adjusted_n_pump_time_ms)))
            client.publish("str/p_pump", str(int(adjusted_p_pump_time_ms)))
            client.publish("str/k_pump", str(int(adjusted_k_pump_time_ms)))
        elif latest_data.ec > target_ec.target_ec + tolerance:
            # Negative control values are not handled for EC in this example
            pass

    return {'status': 'success'}

@shared_task
def adjust_wt():
    latest_data = CalculatedValues.objects.last()
    target_values = TargetWt.objects.last()
    if latest_data and target_values:
        pid_wt.setpoint = target_values.target_water_temp  # Update setpoint from latest data
        control_value = pid_wt(latest_data.water_temp)
        if control_value > 0:
            client.publish("control/water_temp", "wt+")
        elif control_value < 0:
            client.publish("control/water_temp", "wt-")

    return {'status': 'success'}

@shared_task
def adjust_fan_speed():
    latest_data = SensorData2.objects.last()
    target_data = TargetTemp.objects.last()
    
    if latest_data is None:
        logger.error("Keine Sensordaten gefunden.")
        return {'status': 'error', 'message': 'Keine Sensordaten gefunden.'}
    
    if target_data is None:
        logger.error("Keine Zieltemperaturdaten gefunden.")
        return {'status': 'error', 'message': 'Keine Zieltemperaturdaten gefunden.'}
    
    # PID Setpoint aktualisieren
    pid_fan_speed.setpoint = target_data.target_temperature
    
    # Steuerwert berechnen
    control_value = pid_fan_speed((latest_data.temperature1+ latest_data.temperature2) / 2)
    
    # Debug-Ausgaben
    logger.info(f"Aktuelle Temperatur: {latest_data.temperature1}")
    logger.info(f"Zieltemperatur: {target_data.target_temperature}")
    logger.info(f"Berechneter Steuerwert vor Begrenzung: {control_value}")
    
    # Steuerwert auf den Bereich 0-255 begrenzen
    control_value = min(max(int(control_value), 0), 255)
    
    # Weitere Debug-Ausgabe
    logger.info(f"Berechneter Steuerwert nach Begrenzung: {control_value}")
    
    fan_speeds = {
        1: 'control/fan_main',
        2: 'control/fan_temp1',
    }
    
    for fan_id, topic in fan_speeds.items():
        client.publish(topic, str(control_value))
        logger.info(f"PWM-Wert {control_value} an {topic} gesendet")

    return {'status': 'success'}


@shared_task
def adjust_humid():
    tolerance = 1.0  # Toleranz von 1%
    latest_data = SensorData2.objects.last()
    current_phase = CurrentPhase.objects.first()
    phase = current_phase.phase
    params = PHASE_PARAMETERS.get(phase, {})

    if latest_data and current_phase:
        temperature = (latest_data.temperature1 + latest_data.temperature2) / 2
        current_humidity = latest_data.humidity1 + latest_data.humidity2 / 2
        # VPD Berechnung
        svp = 0.6108 * math.exp(17.27 * temperature / (temperature + 237.3))
        vpd = (1 - (current_humidity / 100)) * svp

        # Passenden Ziel-VPD, Ziel-Temperatur und Ziel-Luftfeuchtigkeit basierend auf der Temperatur finden
        target_vpd, target_temp, target_humidity = get_target_params(params['target_params'], temperature)
        
        
        try:
            # Speichern des Zielwertes in der Datenbank
            TargetHumid.objects.create(
                target_humidity=target_humidity,
                timestamp=datetime.now()
            )
        except Exception as e:
            print(f"Fehler beim Speichern des Zielwertes: {e}")

        if current_humidity < target_humidity - tolerance:
            # Luftbefeuchter aktivieren, um die Luftfeuchtigkeit zu erhöhen
            pid_humid.setpoint = target_humidity  # Aktualisiere den Sollwert des PID-Reglers
            control_value_ultra = pid_humid(current_humidity)
            
            # Begrenze den Steuerwert auf den Bereich 0-255
            control_value_ultra = min(max(int(control_value_ultra), 0), 255)
            
            # Sende den PWM-Wert per MQTT für die Luftfeuchtigkeitssteuerung (Ultraschallnebler)
            client.publish("control/ultra", str(control_value_ultra))

            # Aktualisiere den Lüfter zur Verteilung der Feuchtigkeit
            pid_fan_ultra.setpoint = target_humidity
            control_value_fan = pid_fan_ultra(current_humidity)
            control_value_fan = min(max(int(control_value_fan), 0), 255)
            client.publish("control/fan_ultra", str(control_value_fan))

        elif current_humidity > target_humidity + tolerance:
            # Lüfter aktivieren, um die Luftfeuchtigkeit zu senken
            pid_fan_humid.setpoint = target_humidity
            control_value_fan_humid = pid_fan_humid(current_humidity)
            
            # Machen Sie die negativen Werte positiv
            control_value_fan_humid = abs(control_value_fan_humid)
            
            # Begrenze den Steuerwert auf den Bereich 0-255
            control_value_fan_humid = min(max(int(control_value_fan_humid), 0), 255)
            
            # Sende den PWM-Wert per MQTT zur Steuerung der Lüfter
            client.publish("control/fan_humid", str(control_value_fan_humid))
            
            # Luftbefeuchter ausschalten
            client.publish("control/ultra", "0")

    return {'status': 'success'}

# Funktion zum Abrufen der Ziel-VPD, Ziel-Temperatur und der Ziel-Luftfeuchtigkeit basierend auf der Temperatur
def get_target_params(target_params_list, temperature):
    closest_vpd, closest_temp, target_humidity = min(target_params_list, key=lambda x: abs(x[1] - temperature))
    return closest_vpd, closest_temp, target_humidity
            
           

@shared_task
def water_plants_task():
    latest_data = SensorSoilMoisture.objects.last()
    current_phase = CurrentPhase.objects.first()
    phase = current_phase.phase if current_phase else "default_phase"
    params = PHASE_PARAMETERS.get(phase, {})

    target_moisture = params.get('target_moisture', 70)
    min_moisture = params.get('min_moisture', 60)
    max_moisture = params.get('max_moisture', 80)

    if latest_data:
        current_moisture = (latest_data.soil_moisture1 + latest_data.soil_moisture2) / 2

        # Prüfe den letzten Pumpzeitpunkt und die aktuelle Zeit
        pump_status, created = PumpStatus.objects.get_or_create(id=1)
        if datetime.now() < pump_status.last_pump_time + timedelta(minutes=pump_status.wait_minutes):
            return {'status': 'waiting'}

        if current_moisture < min_moisture:
            volume_medium = 3.15  # Liter
            max_water_holding_capacity = 0.85 * volume_medium  # 85% der maximalen Wasseraufnahme
            delta_moisture = target_moisture - current_moisture
            water_needed = (delta_moisture / 100) * max_water_holding_capacity  # Liter
            flow_rate = 2 / 60  # Liter pro Minute
            pump_time = water_needed / flow_rate  # Minuten

            if pump_time > 0:
                client.publish("control/water_control", str(int(pump_time * 60 * 1000)))  # in Millisekunden
                pump_status.last_pump_time = datetime.now()
                pump_status.save()

    return {'status': 'success'}
