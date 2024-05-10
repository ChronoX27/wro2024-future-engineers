from time import sleep
from RPi import GPIO


class DCController:
    def __init__(self, EN: int = 25, IN1: int = 24, IN2: int = 23):
        """pass GPIO pin numbers, not physical pin nubers"""
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
        self.duty_cyle = 0
        self.pwm.start(self.duty_cyle)

    def _drive(self, speed: int):
        """speed (int): -100 to 100
        speed = 0: stops
        speed < 0: drives backwards
        """
        if speed == 0:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            return
        if speed > 0:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            speed = min(speed, 100)
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            speed = min(speed * -1, 100)
        # self.pwm.ChangeDutyCycle(speed)
        self._smooth_acceleration(speed)

    def _smooth_acceleration(self, new_duty_cycle: int):
        while self.duty_cyle - new_duty_cycle > 10:
            if new_duty_cycle > self.duty_cyle:
                self.duty_cyle += 10
            elif new_duty_cycle < self.duty_cyle:
                self.duty_cyle -= 10
            self.pwm.ChangeDutyCycle(self.duty_cyle)
            sleep(0.08)
        while self.duty_cyle != new_duty_cycle:
            if new_duty_cycle > self.duty_cyle:
                self.duty_cyle += 1
            elif new_duty_cycle < self.duty_cyle:
                self.duty_cyle -= 1
            self.pwm.ChangeDutyCycle(self.duty_cyle)
            sleep(0.015)

    def forward(self, speed: int):
        """drives forward
        speed (int): 0 to 100"""
        self._drive(speed)

    def backward(self, speed: int):
        """drives backwards
        speed (int): 0 to 100"""
        self._drive(-speed)

    def stop(self):
        self._drive(0)

    def stop_and_exit(self):
        """cleanup gpio pins"""
        self.stop()
        self.pwm.stop()
        GPIO.cleanup()
        print("dc cleaned, bye :)")
