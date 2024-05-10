import time
from RPi import GPIO


class UltrasonicSensor:
    def __init__(
        self,
        trigger: int,
        echo: int,
        trigger_time: int | float = 0.02,
        timeout: int | float = 0.03,
    ):
        """pass GPIO pin numbers, not physical pin nubers
        trigger_time: time (in s) during which the pin is on
        timeout: time (in s) until the signal is discarded and get_distance returns -1
        """
        self.trigger = trigger
        self.echo = echo
        self.trigger_time = trigger_time
        self.timeout = timeout
        self.last_distance = -1
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def _measure_once(self) -> float:
        """measures the distance to an obstacle and returns it in cm"""
        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(self.trigger_time)
        GPIO.output(self.trigger, GPIO.LOW)

        start_time = time.time()
        stop_time = time.time()
        timeout_start = time.time()

        # save StartTime
        while GPIO.input(self.echo) == GPIO.LOW:
            start_time = time.time()
            if start_time - timeout_start > self.timeout:
                return -1

        # save time of arrival
        while GPIO.input(self.echo) == GPIO.HIGH:
            stop_time = time.time()
            if stop_time - timeout_start > self.timeout:
                return -1

        time_elapsed = stop_time - start_time
        # multiply with the sonic speed (343.2 m/s = 3432 cm/s)
        # and divide by 2, because there and back
        distance = (time_elapsed * 34320) / 2
        return distance

    def get_distance(self) -> float:
        """does three mesaurements to increase precison"""
        d1 = self._measure_once()
        d2 = self._measure_once()
        d3 = self._measure_once()
        d = sorted([d1, d2, d3])

        if d[1] == -1:
            distance = -1
        elif d[0] == -1:
            distance = (d[1] + 0.5 * d[2]) / 1.5
        else:
            distance = (0.5 * d[0] + d[1] + 0.5 * d[2]) / 2
        self.last_distance = round(distance, 2)
        return round(distance, 2)
