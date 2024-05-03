from time import sleep
import RPi.GPIO as GPIO


class ServoController:
    def __init__(
        self,
        pin: int,
        min_angle: int | float = 40,
        max_angle: int | float = 130,
        center_angle: int | float = 90,
    ):
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.center_angle = center_angle
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def set_angle(self, angle: int | float):
        if angle < self.min_angle or angle > self.max_angle:
            return f"Angle {angle}° not in range {self.min_angle}° - {self.max_angle}°"
        duty = angle / 18 + 2
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.pin, False)
        return f"Angle set to {angle}°"

    def set_left(self):
        return self.set_angle(self.min_angle)

    def set_right(self):
        return self.set_angle(self.max_angle)

    def set_center(self):
        return self.set_angle(self.center_angle)

    def stop_pwm(self):
        self.pwm.stop()
        GPIO.cleanup()
        print("servo cleaned :)")


class DCController:
    def __init__(self, EN: int = 25, IN1: int = 24, IN2: int = 23):
        self.EN = EN
        self.IN1 = IN1
        self.IN2 = IN2
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.EN, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)

        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)

        self.pwm = GPIO.PWM(self.EN, 100)
        self.pwm.start(0)

    def drive(self, speed: int):  # , step: float | int = 1
        """speed (int): -100 to 100
        step: drive time in seconds
        speed = 0
        speed < 0 drives backwards
        """
        speed = max(-100, min(speed, 100))
        if speed == 0:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            return
        if speed > 0:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)
        # sleep(step)

    def stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def gpio_exit(self):
        """cleanup gpio pins"""
        self.pwm.stop()
        GPIO.cleanup()
        print("dc cleaned, bye :)")
