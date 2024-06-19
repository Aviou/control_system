from simple_pid import PID

# Initialize PID controllers for N, P, and K
pid_n = PID(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=1.0)  # Beispielwerte
pid_p = PID(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=1.0)  # Beispielwerte
pid_k = PID(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=1.0)  # Beispielwerte
pid_ph = PID(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=7.0)  # Beispielwerte
pid_wt = PID(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=25.0)  # Beispielwerte
pid_fan_speed = PID(Kp=-35.0, Ki=0.1, Kd=0.05, setpoint=20.0, output_limits=(0, 255))  # Beispielwerte für Temperaturregelung
pid_humid = PID(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=60.0, output_limits=(0, 255))
pid_fan_ultra = PID(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=60.0, output_limits=(0, 255))
pid_fan_humid = PID(Kp=1.0, Ki=0.1, Kd=0.05, setpoint=60.0, output_limits=(0, 255))
# Set output limits if needed
pid_n.output_limits = (0, 10000)  # Begrenzung der Pumpzeit in Millisekunden (z.B. bis zu 60 Sekunden)
pid_p.output_limits = (0, 10000)
pid_k.output_limits = (0, 10000)

