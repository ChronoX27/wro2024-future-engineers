import time
import threading
from picarx import Picarx
from stop import reset


px = Picarx()
USE_CAMERA = False
# sensor_data = SensorData()
if USE_CAMERA:
    from vilib import Vilib

    Vilib.camera_start()
    Vilib.display(local=False, web=True)
    Vilib.color_detect_switch(True)
    red = SensorData()
    green = SensorData()


class SensorData:
    """Klasse zum abspeichern und aufrufen von Sensordaten"""

    def __init__(self):
        self.data = -1
        # self.lock = threading.Lock()
        # self.new_data_event = threading.Event()

    def set_data(self, new_data):
        # with self.lock:
        # self.new_data_event.set()
        self.data = new_data

    def get_data(self):
        # with self.lock:
        # self.new_data_event.clear()
        return self.data


# class CameraData:
#     def __init__(self, color) -> None:
#         self.color = color


def read_camera_values(data_class, color):
    """Liest Kamerawerte für eine bestimmte Farbe aus und speichert sie in data_class"""
    while True:
        Vilib.color_detect(color)
        d = {
            "start_x": Vilib.detect_obj_parameter["color_x"],
            "start_y": Vilib.detect_obj_parameter["color_y"],
            "end_x": Vilib.detect_obj_parameter["color_x"]
            + Vilib.detect_obj_parameter["color_w"],
            "end_y": Vilib.detect_obj_parameter["color_y"]
            + Vilib.detect_obj_parameter["color_h"],
            "count": Vilib.detect_obj_parameter["color_n"],
        }
        data_class.set_data(d)
        time.sleep(0.1)


def read_ultrasonic(data_class):
    """Liest die Entfernung per Ultraschall aus und speichert sie in data_class"""
    while True:
        new_data = round(px.ultrasonic.read())  # Sensorwert
        if new_data > 60:
            new_data = 777
        data_class.set_data(new_data)
        time.sleep(0.1)


def read_grayscale(data_class):
    """Liest die Graustufenwerte aus und speichert sie in data_class"""
    while True:
        d = px.get_grayscale_data()
        data_class.set_data(d)
        time.sleep(0.1)


def main(ultrasonic):
    """Hauptschleife des Steuerungscode"""
    # reset(px)
    print("hi")
    power = 10  # Geschwindigkeit des Robos beim Fahren.
    lenkung = 30  # Einschlag des Lenkmotors
    safe = 40  # Sagt dem Robo wie viel Sicherheitsabstand zu Objekten genug ist.
    gefahr = 20  # Sagt dem Robo ab wann er lenken soll

    while True:
        us_distance = ultrasonic.get_data()
        print("us")
        print(us_distance)
        # red_values = red.get_data()
        # print(red_values)
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
            # time.sleep(0.5)


if __name__ == "__main__":
    # if !working:
    #     work()

    ultrasonic = SensorData()
    grayscale = SensorData()
    print("classes - done")

    # Erstelle einen Thread für das Lesen des ultraschallsensor
    ultrasonic_thread = threading.Thread(target=read_ultrasonic, args=(ultrasonic,))
    ultrasonic_thread.daemon = True
    ultrasonic_thread.start()
    print("us - done")

    # Erstelle einen Thread für das Lesen des Grayscale-sensor
    grayscale_thread = threading.Thread(target=read_grayscale, args=(grayscale,))
    grayscale_thread.daemon = True
    grayscale_thread.start()
    print("grayscale - done")

    if USE_CAMERA:
        # Erstelle einen Thread für das Lesen des Grayscale-sensor
        red_detection_thread = threading.Thread(
            target=read_camera_values, args=(red, "red")
        )
        red_detection_thread.daemon = True
        red_detection_thread.start()
        print("cam detection - done")
    else:
        red = -1
    # main(sensor_data)

    # try:
    print("starting main...")
    main(ultrasonic)
    # except Exception as e:
    #     print(e)
    #     reset(px)
    #     Vilib.camera_close()
