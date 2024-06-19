from django.db import models

class SensorData(models.Model):
    raw_ph_voltage = models.FloatField()
    raw_ec_voltage = models.FloatField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
   

class CalculatedValues(models.Model):
    ph = models.FloatField()
    ec = models.FloatField()
    water_temp =models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        get_latest_by = 'timestamp'

class TargetPh(models.Model):
    target_ph = models.FloatField()
    pump_time_ph = models.FloatField()  
    timestamp = models.DateTimeField(auto_now_add=True)

class TargetEc(models.Model):
    target_ec = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class TargetRatio(models.Model):
    n_ratio = models.FloatField()
    p_ratio = models.FloatField()
    k_ratio = models.FloatField()
    pump_time_ratio = models.FloatField()  # in Sekunden
    timestamp = models.DateTimeField(auto_now_add=True)

class TargetWt(models.Model):
    target_water_temp = models.FloatField() 
    timestamp = models.DateTimeField(auto_now_add=True)


class TargetTemp(models.Model):
    target_temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class TargetHumid(models.Model):
    target_humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class SensorData2(models.Model):
    temperature1 = models.FloatField()
    temperature2 = models.FloatField()
    humidity1 = models.FloatField()
    humidity2 = models.FloatField()
    pressure1 = models.FloatField()
    pressure2 = models.FloatField()
    waterTemp1 = models.FloatField()
    waterTemp2 = models.FloatField()
    distance = models.FloatField()
    flowRate = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        get_latest_by = 'timestamp'  

class SensorSoilMoisture(models.Model):
    soilMoisture1 = models.FloatField()
    soilMoisture2 = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        get_latest_by = 'timestamp'

class WaterLevelHumid(models.Model):
    water_level = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class WaterVolume(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    volume = models.FloatField()

    def __str__(self):
        return f"{self.volume} liters at {self.timestamp}"

class CurrentPhase(models.Model):
    phase = models.CharField(max_length=20, default='wachstum')

    def __str__(self):
        return self.phase
    
class PumpStatus(models.Model):
    is_active = models.BooleanField(default=False)
    last_pump_time = models.DateTimeField(null=True, blank=True)

class SensorDataOutdoor(models.Model):
    temperature01 = models.FloatField()
    humidity01 = models.FloatField()
    temperature02 = models.FloatField()
    humidity02 = models.FloatField()
    temperature03 = models.FloatField()
    humidity03 = models.FloatField()
    soil_temp01 = models.FloatField()
    soil_temp02 = models.FloatField()
    soil_temp03 = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        get_latest_by = 'timestamp'                              

class SensorMoisture(models.Model):
    moisture01 = models.FloatField()
    moisture02 = models.FloatField()
    moisture03 = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        get_latest_by = 'timestamp'

class CalibrationEc(models.Model):
    ec1 = models.FloatField()
    ec5 = models.FloatField()
    ec12 = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class CalibrationPh(models.Model):
    ph4 = models.FloatField()
    ph7 = models.FloatField()
    ph9 = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  

class GrenzwerteSensorPh(models.Model):
    ph_min = models.FloatField()
    ph_max = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    class Meta:
        get_latest_by = 'timestamp'

class GrenzwerteSensorEc(models.Model):
    ec_min = models.FloatField()
    ec_max = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    class Meta:
        get_latest_by = 'timestamp'

class GrenzwerteSensorTemp(models.Model):
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    class Meta:
        get_latest_by = 'timestamp'

class GrenzwerteSensorHumd(models.Model):
    humd_min = models.FloatField()  
    humd_max = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    class Meta:
        get_latest_by = 'timestamp'

class GrenzwerteSensorWt(models.Model):
    temp_wt_min = models.FloatField(default=0)
    temp_wt_max = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True) 
    class Meta:
        get_latest_by = 'timestamp'

class GrenzwerterSensorGas(models.Model):
    gas_grenzwert = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    class Meta:
        get_latest_by = 'timestamp'

class GrenzwerteWaterflow(models.Model):
    waterflow_grenzwert = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True) 
    class Meta:
        get_latest_by = 'timestamp'

class Relay(models.Model):
    name = models.CharField(max_length=50)
    run_time = models.IntegerField(default=0)  # in Sekunden
    pause_time = models.IntegerField(default=0)  # in Sekunden

    def __str__(self):
        return self.name