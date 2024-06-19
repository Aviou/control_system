from .models import SensorData2
import time

# Abmessungen des Tanks in cm
tank_length = 40  # cm
tank_width = 30  # cm
tank_height = 42  # cm

def update_remaining_water_volume():
    global remaining_water_volume

    # Letzte Sensor-Daten abrufen
    sensor_data = SensorData2.objects.order_by('-id').first()
    
    if sensor_data:
        # Abstand von der Oberseite des Tanks zur Wasseroberfläche in cm
        distance = sensor_data.distance

        # Berechnung der Wasserhöhe
        water_height = tank_height - distance  # cm

        if water_height < 0:
            water_height = 0
        elif water_height > tank_height:
            water_height = tank_height

        # Berechnung des Wasservolumens in Litern
        remaining_water_volume = (tank_length * tank_width * water_height) / 1000  # cm³ zu Litern
        return remaining_water_volume
    else:
        return 0


