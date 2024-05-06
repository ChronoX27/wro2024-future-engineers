from time import sleep
from dc_controller import DCController
from servo_controller import ServoController
from ultrasonic_sensor import UltrasonicSensor

# PINs
LENKUNG = 16
DC_ENB = 25
DC_IN3 = 24
DC_IN4 = 23

servo = ServoController(LENKUNG)
dc = DCController(DC_ENB, DC_IN3, DC_IN4)
us_left = UltrasonicSensor(17, 0)
us_mid = UltrasonicSensor(27, 5)
us_right = UltrasonicSensor(22, 6)

try:
    sleep(15)
    i = 0
    while i < 5:
        print(us_mid.get_distance())
        dc.backward(30)
        sleep(3)
        dc.forward(40)
        sleep(1)
        servo.set_angle(20)
        sleep(2)
        servo.set_center()
        dc.forward(10)
        sleep(5)
        dc.backward(40)
        servo.set_right()
        sleep(1)
        dc.forward(20)
        i += 1
finally:
    dc.gpio_exit()
    servo.stop_and_clean()
