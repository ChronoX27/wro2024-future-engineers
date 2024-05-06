from time import sleep
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

    def set_angle(self, angle: int | float) -> str:
        if angle < self.min_angle or angle > self.max_angle:
            new_angle = max(self.min_angle, min(angle, self.max_angle))
            message = (
                f"Angle {new_angle}° not in range {self.min_angle}° - {self.max_angle}°"
            )
        else:
            new_angle = angle
            message = f"Angle set to {angle}°"
        duty = new_angle / 18 + 2
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.pin, False)
        return message

    def set_left(self) -> str:
        return self.set_angle(self.min_angle)

    def set_right(self) -> str:
        return self.set_angle(self.max_angle)

    def set_center(self) -> str:
        return self.set_angle(self.center_angle)

    def stop_and_clean(self):
        self.pwm.stop()
        GPIO.cleanup()
        print("servo cleaned :)")
