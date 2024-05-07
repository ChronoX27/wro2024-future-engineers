from RPi import GPIO


class ServoController:
    def __init__(
        self,
        pin: int,
        min_angle: int | float = 40,
        max_angle: int | float = 130,
        center_angle: int | float = 90,
    ):
        """pass GPIO pin numbers, not physical pin nubers"""
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
        self.set_center()

    def set_angle(self, angle: int | float) -> None:
        new_angle = max(self.min_angle, min(angle, self.max_angle))
        duty = new_angle / 18 + 2
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        GPIO.output(self.pin, False)
        return

    def set_left(self):
        self.set_angle(self.min_angle)

    def set_right(self):
        self.set_angle(self.max_angle)

    def set_center(self):
        self.set_angle(self.center_angle)

    def stop_and_clean(self):
        self.set_center()
        self.pwm.stop()
        GPIO.cleanup()
        print("servo cleaned :)")
