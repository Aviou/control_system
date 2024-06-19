from django.contrib import admin
from .models import SensorData, TargetEc, TargetPh, TargetRatio, CalculatedValues, TargetWt

admin.site.register(SensorData)
admin.site.register(TargetEc)
admin.site.register(TargetPh)
admin.site.register(TargetWt)
admin.site.register(TargetRatio)
admin.site.register(CalculatedValues)