import numpy as np
from .models import CalibrationPh, CalibrationEc, SensorData2
from django.core.exceptions import ObjectDoesNotExist

# Konstanten für die Nernst-Gleichung
R = 8.314  # Gaskonstante, J/(mol·K)
F = 96485  # Faraday-Konstante, C/mol
T_standard = 298.15  # Standardtemperatur in Kelvin (25 °C)

def load_latest_calibration():
    try:
        latest_ph_calibration = CalibrationPh.objects.latest('timestamp')
        kalibrierung_punkte = np.array([
            (4.01, latest_ph_calibration.ph4), 
            (6.88, latest_ph_calibration.ph7), 
            (9.18, latest_ph_calibration.ph9)
        ])
    except ObjectDoesNotExist:
        # Setze Standardwerte oder behandele das Fehlen von Daten
        kalibrierung_punkte = np.array([])
    
    try:
        latest_ec_calibration = CalibrationEc.objects.latest('timestamp')
        ec_calibration_points = np.array([
            (1.5, latest_ec_calibration.ec1), 
            (8.5, latest_ec_calibration.ec5), 
            (12.88, latest_ec_calibration.ec12)
        ])
    except ObjectDoesNotExist:
        # Setze Standardwerte oder behandele das Fehlen von Daten
        ec_calibration_points = np.array([])
    
    return kalibrierung_punkte, ec_calibration_points

def berechne_ph_wert(spannung, temperatur):
    kalibrierung_punkte, _ = load_latest_calibration()
    if kalibrierung_punkte.size == 0:
        return np.nan  
    ph_werte, spannungen = kalibrierung_punkte[:, 0], kalibrierung_punkte[:, 1]
    grad_des_polynoms = 2
    koeffizienten = np.polyfit(spannungen, ph_werte, grad_des_polynoms)
    polynom = np.poly1d(koeffizienten)

    T_kelvin = temperatur + 273.15  # Umrechnung in Kelvin
    pH_bei_standard_temp = polynom(spannung)
    ph1 = pH_bei_standard_temp - ((T_kelvin - T_standard) * (2.303 * R) / F) / (2.303 * R / F * T_standard)
    ph = np.median(ph1)
    return np.round(ph, 2)

def berechne_ec(spannung, temperatur, temp_koeff=0.02, standard_temp=25):
    _, ec_calibration_points = load_latest_calibration()
    if ec_calibration_points.size == 0:
        return np.nan 
    ec_werte, spannungen = ec_calibration_points[:, 0], ec_calibration_points[:, 1]
    grad_des_polynoms = 2
    ec_koeffizienten = np.polyfit(spannungen, ec_werte, grad_des_polynoms)
    ec_polynom = np.poly1d(ec_koeffizienten)

    ec_gemessen = ec_polynom(spannung)
    ec1 = ec_gemessen * (1 + temp_koeff * (temperatur - standard_temp))
    ec = np.median(ec1)
    return np.round(ec, 2)

