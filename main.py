import time
import threading
from picarx import Picarx
from vilib import Vilib


px = Picarx()
picar_2 = Picarx(ultrasonic_pins=["D0", "D1"])  # Test um neuen Sensor zu verwenden
Vilib.camera_start(vflip=False, hflip=False)
Vilib.display(local=False, web=True)


class SensorData:
    """Klasse zum abspeichern und aufrufen von Sensordaten"""

    def __init__(self, default_value: int | float = 0):
        self.data = default_value

    def read(self) -> int | float:
        return self.data

    def set(self, value: int | float):
        self.data = value


def distance(picar: Picarx, dist: SensorData) -> None:
    while True:
        dist.set(picar.ultrasonic.read())
        time.sleep(0.1)


def colorfinder(red: SensorData, green: SensorData) -> None:
    while True:
        Vilib.color_detect("red")
        red.set(Vilib.detect_obj_parameter["color_n"])
        time.sleep(0.1)
        Vilib.color_detect("green")
        green.set(Vilib.detect_obj_parameter["color_n"])
        time.sleep(0.1)


if __name__ == "__main__":
    #### SENSOR-THREADS ####
    distance_data = SensorData(100)
    found_red = SensorData(0)
    found_green = SensorData(0)

    us_thread = threading.Thread(target=distance, args=(px, distance_data))
    us_thread.start()
    cam_thread = threading.Thread(target=colorfinder, args=(found_red, found_green))
    cam_thread.start()

    #### SETUP ####
    STEP = 10
    LENKUNG = 50
    GEFAHR = 35
    ACHTUNG = 40
    OFFSET = 10  # falls die Achsen nicht gerade sind

    time_to_next = 0.5

    print("Set servos to zero")
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    px.set_dir_servo_angle(0)

    while True:

        us_distance = distance_data.read()
        print(found_red.read(), found_green.read(), us_distance)

        if us_distance <= GEFAHR:
            print("stop. hindernis einlenken")
            px.set_dir_servo_angle(-LENKUNG - OFFSET)
            px.forward(STEP)
            time_to_next = 0.7
        elif us_distance <= ACHTUNG:
            if found_red.read() > found_green.read():
                print("rechts weil grün")
                px.set_dir_servo_angle(-LENKUNG - OFFSET)
                px.forward(STEP)
                time_to_next = 0.5
            elif found_green.read() > found_red.read():
                print("links weil rot")
                px.set_dir_servo_angle(LENKUNG - OFFSET)
                px.forward(STEP)
                time_to_next = 0.5
            else:
                print("weiter")
                px.set_dir_servo_angle(0 - OFFSET)
                px.forward(STEP)
                time_to_next = 0.1
        else:
            print("weiter, zu weit weg")
            px.set_dir_servo_angle(0 - OFFSET)
            px.forward(STEP)
            time_to_next = 0.1

        time.sleep(time_to_next)
