import time
import threading
from picarx import Picarx
from vilib import Vilib

Vilib.camera_start(vflip=False, hflip=False)
Vilib.display(local=True, web=True)

px = Picarx()

class SensorData:
    def __init__(self):
        self.data = 0
    def read(self):
        return self.data
    def set(self, value):
        self.data = value

def distance(px, distance):
    while True:
        d.set(px.ultrasonic.read())
        time.sleep(0.1)

def colorfinder(px, found_red, found_green):
    while True:
        Vilib.color_detect('red')
        found_red.set(Vilib.detect_obj_parameter["color_n"])
        time.sleep(0.1)
        Vilib.color_detect('green')
        found_green.set(Vilib.detect_obj_parameter["color_n"])
        time.sleep(0.1)

if __name__ == "__main__":
    d = SensorData()
    found_red = SensorData()
    found_green = SensorData()

    thread1 = threading.Thread(target=distance, args=(px, d))
    thread2 = threading.Thread(target=colorfinder, args=(px, found_red, found_green))

    thread1.start()
    thread2.start()

    while True:

        print(found_red.read(), found_green.read(), d.read())

        if d.read() <= 10:
            print("stop. zu nah dran. einlenken")
            px.set_dir_servo_angle(-90)
            px.forward(10)
        elif d.read() <= 30:
            if found_red.read() > found_green.read():
                print("rechts weil grün")
                px.set_dir_servo_angle(-90)
                px.forward(10)
            elif found_green.read() > found_red.read():
                print("links weil rot")
                px.set_dir_servo_angle(90)
                px.forward(20)
            else:
                print("weiter")
                px.set_dir_servo_angle(0)
                px.forward(20)
        else:
            print("weiter, zu weit weg")
            px.set_dir_servo_angle(0)
            px.forward(20)


        time.sleep(1)