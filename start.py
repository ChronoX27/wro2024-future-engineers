from time import sleep
from RPi import GPIO

BUTTON = 2
LED = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN)

sleep(3)
GPIO.output(LED, GPIO.HIGH)

# button nicht gedrückt
while GPIO.input(BUTTON) == GPIO.LOW:
    sleep(0.2)

# Button wird gedrückt
GPIO.output(LED, GPIO.LOW)
sleep(2)
# Programm Hauptschleife wird bei import ausgeführt...
import main  # NICHT VERSCHIEBEN (bitte)

print(main.DC_IN4)
