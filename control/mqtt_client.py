import paho.mqtt.client as mqtt
import json
import logging
import threading
from .models import SensorData2
import requests

client = mqtt.Client()

wifi_ssid = 'FRITZ!Box 6660 Cable QH'
wifi_password = '96227716202647739666'

# MQTT-Broker-Einstellungen
mqtt_broker = '192.168.178.43'
mqtt_port = 1884



# Einrichten des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected with result code {rc}")
    client.subscribe("data/phecwt")
    client.subscribe("all_calibration/volts")
    client.subscribe("sensor/data")
    client.subscribe("sensor/outdoor")  
    client.subscribe("sensor/water_level")
    client.subscribe("sensor/soil")
        
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        # URL der Django-View, die die Daten verarbeitet
        url = 'http://localhost:8000/sensor-data-view/'  # Passen Sie die URL entsprechend an

        headers = {'Content-Type': 'application/json'}
        
        # Senden einer POST-Anfrage an die Django-View
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            logger.info("Daten erfolgreich an Django gesendet.")
        else:
            logger.error(f"Fehler beim Senden der Daten an Django: {response.status_code}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


def start_mqtt_client():
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(mqtt_broker, mqtt_port, 60)
        client.loop_forever()  # Verwendet loop_forever anstelle von loop_start
        logger.info("MQTT client connected and loop started.")
    except Exception as e:
        logger.error(f"Error connecting to MQTT broker: {e}")

# Starte den MQTT-Client in einem separaten Thread
mqtt_thread = threading.Thread(target=start_mqtt_client)
mqtt_thread.start()
