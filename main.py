import time
import threading
from picarx import Picarx
from robot_hat import Servo
from robot_hat.utils import reset_mcu


class SensorData:
    def __init__(self):
        self.data = None
        self.lock = threading.Lock()
        self.new_data_event = threading.Event()

    def set_data(self, new_data):
        # with self.lock:
        # self.new_data_event.set()
        self.data = new_data

    def get_data(self):
        # with self.lock:
        # self.new_data_event.clear()
        return self.data


def read_ultrasonic(data):
    while True:
        new_data = round(px.ultrasonic.read())  # Sensorwert
        if new_data > 60:
            new_data = -1
        data.set_data(new_data)
        time.sleep(0.1)


def reset():
    """Resettet alle Motoren."""
    print("Set servos to zero")
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    px.set_dir_servo_angle(0)
    reset_mcu()
    for i in range(12):
        Servo(i).angle(10)
        time.sleep(0.1)
        Servo(i).angle(0)
        time.sleep(0.1)


def main(data):
    """Hauptschleife für den Roboter"""
    reset()

    power = 50  # Geschwindigkeit des Robos beim Fahren.
    lenkung = 30  # Einschlag des Lenkmotors
    safe = 40  # Sagt dem Robo wie viel Sicherheitsabstand zu Objekten genug ist.
    gefahr = 20  # Sagt dem Robo ab wann er lenken soll

    while True:
        us_distance = data.get_data()
        print(us_distance)
        # Gerade aus fahren wenn sicht frei ist.
        if us_distance >= safe:
            px.set_dir_servo_angle(0)
            px.forward(power)
        # Wird gefährlich, Richtung ändern. (Wand oder Hinderniss zu nah)
        elif us_distance >= gefahr:
            print("lenkmanöver")
            px.set_dir_servo_angle(lenkung)
            px.forward(power)
            time.sleep(0.1)
        # Kein Ausweg mehr, Robo ist zu nah am Hindernis oder der Wand um zu fahren.
        else:
            print("zurück")
            # px.set_dir_servo_angle(-lenkung)
            px.backward(power)
            time.sleep(0.5)


px = Picarx()
sensor_data = SensorData()

# if !working:
#     work()

# Erstelle einen Thread für das Lesen des Sensors
sensor_thread = threading.Thread(target=read_ultrasonic, args=(sensor_data,))
sensor_thread.daemon = True  # Stellt sicher, dass der Thread im Hintergrund läuft
sensor_thread.start()

main(sensor_data)
