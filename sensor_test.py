from time import sleep
from picarx import Picarx

px = Picarx()
while True:
    print(px.ultrasonic.read())
    sleep(1)
