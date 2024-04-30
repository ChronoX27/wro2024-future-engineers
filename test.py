from time import sleep
import RPi.GPIO as GPIO

ENA = 25
IN_1 = 24
IN_2 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN_1, GPIO.OUT)
GPIO.setup(IN_2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.output(IN_1, GPIO.LOW)
GPIO.output(IN_2, GPIO.LOW)
p = GPIO.PWM(ENA, 100)
p.start(25)


def forward(speed: int, step: float | int):
    """speed (int): 0 - 100
    step: drive time in seconds
    """
    GPIO.output(IN_1, GPIO.HIGH)
    GPIO.output(IN_2, GPIO.LOW)
    if speed > 100:
        speed = 100
    if speed < 0:
        speed = 0
    p.ChangeDutyCycle(speed)
    sleep(step)


def backward(speed: int, step: float | int):
    """speed (int): 0 - 100"""
    GPIO.output(IN_1, GPIO.LOW)
    GPIO.output(IN_2, GPIO.HIGH)
    if speed > 100:
        speed = 100
    if speed < 0:
        speed = 0
    p.ChangeDutyCycle(speed)
    sleep(step)


def stop():
    GPIO.output(IN_1, GPIO.LOW)
    GPIO.output(IN_2, GPIO.LOW)

def gpio_exit():
    GPIO.cleanup()
    print("bye :)")

if __name__ == "__main__":
    print("\nThe default speed & direction of motor is Low & Forward.....")
    print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit\n")

    while True:
        x = input()

        if x == "s":
            stop()
        elif x == "f":
            forward(50, 1)
        elif x == "b":
            backward(50, 1)
        elif x == "l":
            forward(25, 1)
        elif x == "m":
            forward(50, 1)
        elif x == "h":
            forward(75, 1)
        elif x == "+":
            forward(100, 1)
        elif x == "e":
            gpio_exit()
            break
        else:
            print(">> try again")
