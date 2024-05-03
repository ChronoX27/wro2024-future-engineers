from time import sleep
from motors import ServoController, DCController

# PINs
LENKUNG = 17
DC_ENA = 25
DC_IN1 = 24
DC_IN2 = 23

servo = ServoController(LENKUNG)
dc = DCController(DC_ENA, DC_IN1, DC_IN2)

try:
    for i in range(5):
        dc.drive(50)
        servo.set_left()
        sleep(0.5)
        servo.set_center()
        sleep(1)
        servo.set_right()
        sleep(0.5)
        servo.set_center()
        sleep(1)
finally:
    dc.gpio_exit()
    servo.stop_pwm()
