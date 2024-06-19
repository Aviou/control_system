
from telegram import Bot
from telegram.error import TelegramError
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import asyncio
from datetime import timedelta
from django.utils import timezone
from .models import CalculatedValues,SensorData, GrenzwerteSensorWt, GrenzwerteSensorEc, GrenzwerteSensorHumd, GrenzwerteSensorPh, GrenzwerteWaterflow, GrenzwerteSensorTemp, SensorData2, GrenzwerterSensorGas
from asgiref.sync import sync_to_async

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_id = 1178471350  # Chat-ID des Empfängers
bot_token = '7030942913:AAH7tFNhq2fwy_lM95jIP9CaAhiJ0B3RQoY'
bot = Bot(token=bot_token)

async def send_telegram_message(chat_id, message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Nachricht gesendet an {chat_id}: {message}")
    except Exception as e:
        logger.error(f"Fehler beim Senden der Nachricht: {e}")


async def check_ph_values():
    while True:   # Angenommen, du hast ein Model SensorData mit den Feldern value und threshold
        sensor_data = await sync_to_async(CalculatedValues.objects.latest)()
        latest_grenzwerte_ph = await sync_to_async(GrenzwerteSensorPh.objects.last)()
   
        if sensor_data is not None and latest_grenzwerte_ph is not None:
            if sensor_data.ph > latest_grenzwerte_ph.ph_max:
                    message = f"Warnung: Der Wert von {sensor_data.ph} hat den Grenzwert überschritten! Wert: {latest_grenzwerte_ph.ph_max}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

            elif  sensor_data.ph < latest_grenzwerte_ph.ph_min:
                    message = f"Warnung: Der Wert von {sensor_data.ph} hat den Grenzwert unterschritten! Wert: {latest_grenzwerte_ph.ph_min}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)
            
        await asyncio.sleep(60)

    


    
async def check_ec_values():
    while True:   # Angenommen, du hast ein Model SensorData mit den Feldern value und threshold
        sensor_data = await sync_to_async(CalculatedValues.objects.latest)()
        latest_grenzwerte_ec = await sync_to_async(GrenzwerteSensorEc.objects.last)()

    
        if sensor_data is not None and latest_grenzwerte_ec is not None:
            if sensor_data.ec > latest_grenzwerte_ec.ec_max:
                    message = f"Warnung: Der Wert von {sensor_data.ec} hat den Grenzwert überschritten! Wert: {latest_grenzwerte_ec.ec_max}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

            elif  sensor_data.ec < latest_grenzwerte_ec.ec_min:
                    message = f"Warnung: Der Wert von {sensor_data.ec} hat den Grenzwert unterschritten! Wert: {latest_grenzwerte_ec.ec_min}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)
        await asyncio.sleep(60)


async def check_water_stand():
    while True:   # Angenommen, du hast ein Model SensorData mit den Feldern value und threshold
        sensor2_data = await sync_to_async(SensorData2.objects.latest)()

        if sensor2_data is not None:
            if sensor2_data.water_level == "Kein Wasser":
                    message = f"Wasserstand ist zu niedrig!"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

        await asyncio.sleep(60)

async def check_temp_values():
    while True: 
        latest_grenzwerte_temp = await sync_to_async(GrenzwerteSensorTemp.objects.last)()
        sensor2_data = await sync_to_async(SensorData2.objects.latest)()

        if sensor2_data is not None and latest_grenzwerte_temp is not None:
            if sensor2_data.temperature1 > latest_grenzwerte_temp.temp_max:
                    message = f"Warnung: Der Wert von {sensor2_data.temperature1} hat den Grenzwert überschritten! Wert: {latest_grenzwerte_temp.temp_max}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)
            elif sensor2_data.temperature1 < latest_grenzwerte_temp.temp_min:
                    message = f"Warnung: Der Wert von {sensor2_data.temperature1} hat den Grenzwert unterschritten! Wert: {latest_grenzwerte_temp.temp_min}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

            if sensor2_data.temperature2 > latest_grenzwerte_temp.temp_max:
                    message = f"Warnung: Der Wert von {sensor2_data.temperature2} hat den Grenzwert überschritten! Wert: {latest_grenzwerte_temp.temp_max}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

            elif sensor2_data.temperature2 < latest_grenzwerte_temp.temp_min:
                    message = f"Warnung: Der Wert von {sensor2_data.temperature2} hat den Grenzwert unterschritten! Wert: {latest_grenzwerte_temp.temp_min}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)
        await asyncio.sleep(60)



async def check_humd_values():
    while True:    
        latest_grenzwerte_humd = await sync_to_async(GrenzwerteSensorHumd.objects.last)()
        sensor2_data = await sync_to_async(SensorData2.objects.latest)()

        if sensor2_data is not None and  latest_grenzwerte_humd is not None:

            if sensor2_data.humidity1 > latest_grenzwerte_humd.humd_max:
                    message = f"Warnung: Der Wert von {sensor2_data.humidity1} hat den Grenzwert überschritten! Wert: {latest_grenzwerte_humd.humd_max}"
                    await send_telegram_message(chat_id,  message)
                    logger.info(message)

            elif  sensor2_data.humidity1 < latest_grenzwerte_humd.humd_min:
                    message = f"Warnung: Der Wert von {sensor2_data.humidity1} hat den Grenzwert unterschritten! Wert: {latest_grenzwerte_humd.humd_min}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)
            
            if sensor2_data.humidity2 > latest_grenzwerte_humd.humd_max:
                    message = f"Warnung: Der Wert von {sensor2_data.humidity2} hat den Grenzwert überschritten! Wert: {latest_grenzwerte_humd.humd_max}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

            elif  sensor2_data.humidity2 < latest_grenzwerte_humd.humd_min:
                    message = f"Warnung: Der Wert von {sensor2_data.humidity2} hat den Grenzwert unterschritten! Wert: {latest_grenzwerte_humd.humd_min}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

        await asyncio.sleep(60)



async def check_wt_values():    
    while True:
        latest_grenzwerte_wt = await sync_to_async(GrenzwerteSensorWt.objects.last)() 
        sensor2_data = await sync_to_async(SensorData2.objects.latest)()

        
        if sensor2_data is not None and latest_grenzwerte_wt is not None:

                if sensor2_data.waterTemp1 > latest_grenzwerte_wt.temp_wt_max:
                    message = f"Warnung: Der Wert von {sensor2_data.waterTemp1} hat den Grenzwert überschritten! Wert: {latest_grenzwerte_wt.temp_wt_max}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

                elif  sensor2_data.waterTemp1 < latest_grenzwerte_wt.temp_wt_min:
                    message = f"Warnung: Der Wert von {sensor2_data.waterTemp1} hat den Grenzwert unterschritten! Wert: {latest_grenzwerte_wt.temp_wt_min}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)
            
                if sensor2_data.waterTemp2 > latest_grenzwerte_wt.temp_wt_max:
                    message = f"Warnung: Der Wert von {sensor2_data.waterTemp2} hat den Grenzwert überschritten! Wert: {latest_grenzwerte_wt.temp_wt_max}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

                elif  sensor2_data.waterTemp2 < latest_grenzwerte_wt.temp_wt_min:
                    message = f"Warnung: Der Wert von {sensor2_data.waterTemp2} hat den Grenzwert unterschritten! Wert: {latest_grenzwerte_wt.temp_wt_min}"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

        await asyncio.sleep(60)

async def check_gas_values():    
    while True:
        latest_grenzwerte_gas = await sync_to_async(GrenzwerterSensorGas.objects.last)() 
        sensor2_data = await sync_to_async(SensorData2.objects.latest)()

        
        if sensor2_data is not None and latest_grenzwerte_gas is not None:

                if sensor2_data.sensor_gas > latest_grenzwerte_gas.gas_grenzwert:
                    message = f"Warnung: Feuergefahr!"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

            

        await asyncio.sleep(60)

async def check_waterflow_values():    
    while True:
        latest_grenzwerte_waterflow = await sync_to_async(GrenzwerteWaterflow.objects.last)() 
        sensor2_data = await sync_to_async(SensorData2.objects.latest)()

        
        if sensor2_data is not None and latest_grenzwerte_waterflow is not None:

                if sensor2_data.Waterflow > latest_grenzwerte_waterflow.waterflow_grenzwert:
                    message = f"Warnung: Zu wenig Waserfluss!"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

            

        await asyncio.sleep(60)

async def check_light_values():    
    while True:
        sensor2_data = await sync_to_async(SensorData2.objects.latest)()

        
        if sensor2_data is not None:

                if sensor2_data > latest_grenzwerte_waterflow.waterflow_grenzwert:
                    message = f"Warnung: Zu wenig Waserfluss!"
                    await send_telegram_message(chat_id, message)
                    logger.info(message)

            

        await asyncio.sleep(60)

async def send_warning_message():
    message = "Das Sensor System ist möglicherweise down. Die Daten wurden seit längerem nicht aktualisiert."
    await send_telegram_message(chat_id, message)

async def send_warning2_message():
    message = "Das Main System ist möglicherweise down. Die Daten wurden seit längerem nicht aktualisiert."
    await send_telegram_message(chat_id, message)

async def check_data_continuity():
    while True:
        # Angenommen, Ihr Modell SensorData2 hat ein Feld 'updated_at' für den Zeitstempel der letzten Aktualisierung
        last_sensor_data = await sync_to_async(SensorData2.objects.latest)('timestamp')
        last_update_time = last_sensor_data.timestamp if last_sensor_data else None
        last_raw_data = await sync_to_async(SensorData.objects.latest)('timestamp')
        last_updated_time = last_raw_data.timestamp if last_raw_data else None

        if last_update_time or last_updated_time:
            # Verwendung von timezone.now() um eine korrekte Zeitzone-bewusste Vergleichsoperation zu haben
            if timezone.now() - last_update_time > timedelta(minutes=30):  # Angenommen, 30 Minuten sind zu lang
                await send_warning_message()

            if timezone.now() - last_updated_time > timedelta(minutes=30):
                await send_warning2_message()

        # Warten, bevor die Schleife erneut ausgeführt wird
        await asyncio.sleep(300)  # Alle 5 Minuten überprüfen
       
async def main():
    # Startet alle Überprüfungsfunktionen gleichzeitig
    await asyncio.gather(
        check_ph_values(),
        check_wt_values(),
        check_ec_values(),
        check_temp_values(),
        check_humd_values(),
        check_water_stand(),
        check_data_continuity()  
    )
    
if __name__ == '__main__':
    asyncio.run(main())
