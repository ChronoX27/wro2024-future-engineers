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
        self.pwm.start(0)

    def drive(self, speed: int):  # , step: float | int = 1
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
        self.pwm.ChangeDutyCycle(speed)
        # sleep(step)

    def backwards(self, speed: int):
        """drives backwards
        speed (int): 0 to 100"""
        speed = max(0, min(speed, 100))
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def gpio_exit(self):
        """cleanup gpio pins"""
        self.pwm.stop()
        GPIO.cleanup()
        print("dc cleaned, bye :)")
