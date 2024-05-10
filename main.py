from time import sleep
from dc_controller import DCController
from servo_controller import ServoController
from ultrasonic_sensor import UltrasonicSensor

# PINs
LENKUNG = 16
DC_ENB = 25
DC_IN3 = 24
DC_IN4 = 23

servo = ServoController(LENKUNG)
dc = DCController(DC_ENB, DC_IN3, DC_IN4)
us_left = UltrasonicSensor(17, 0)
us_mid = UltrasonicSensor(27, 5)
us_right = UltrasonicSensor(22, 6)


def get_sensor_data() -> tuple[float, float, float]:
    dist_left = us_left.get_distance()  # 0.08 s
    dist_mid = us_mid.get_distance()
    dist_right = us_right.get_distance()
    return dist_left, dist_mid, dist_right


def steer_dir(direction: int, turn_factor: float = 1):
    """Steuert anhand der Richtungszahl"""
    if direction == 0:
        servo.set_center()
        return
    if direction == -1 and turn_factor == 1:
        servo.set_left()
        return
    if direction == 1 and turn_factor == 1:
        servo.set_right()
        return

    angle = servo.center_angle + direction * turn_factor * (
        servo.max_angle - servo.center_angle
    )
    servo.set_angle(angle)


STATE = "looking"
"""state kann folgende Werte haben:
looking - Herausfinden, ob der Parkour mit oder gegen den Uhrzeigersinn läuft 
turning - Drehen in einer Kurve 
following - Der Wand folgen bis zur nächsten Kurve (Abstand: 5-10cm)
"""
DANGER = 10
SPEED = 30
CURVE_SPEED = 50  # schneller werden in der Kurve
MAX_WALL_DIST = 10
MIN_WALL_DIST = 5

try:
    DIRECTION = 0
    """-1 - links 
    0 - gerade 
    1 - rechts"""
    dc.forward(30)
    servo.set_center()
    # Links oder rechts herum?
    while STATE == "looking":
        left, mid, right = get_sensor_data()
        print(f"{left}\t{mid}\t{right}")
        if left == -1:
            DIRECTION = -1
            STATE = "turning"
        elif right == -1:
            DIRECTION = 1
            STATE = "turning"
        elif mid < DANGER:
            dc.backward(SPEED)
        sleep(0.1)

    print(STATE)
    # Hauptschleife, nachdem die Richtung klar ist
    while True:
        sensor_data = get_sensor_data()
        """sensor_data[-DIRECTION + 1] - Sensor in der Außenkurve
           sensor_data[DIRECTION + 1] - Sensor in der Innenkurve"""
        match (STATE):
            case "turning":
                # Wand vorne erkannt
                if sensor_data[0] < DANGER:
                    dc.backward(CURVE_SPEED)
                    steer_dir(-DIRECTION)
                    sleep(0.1)
                    break
                # Innenwand wird wieder erkannt
                if sensor_data[DIRECTION + 1] != -1:
                    STATE = "following"
                    print(STATE)
                    sleep(0.2)
                    break
                dc.forward(CURVE_SPEED)
                steer_dir(DIRECTION)
            case "following":
                # hält den Abstand zur Wand ein
                if sensor_data[-DIRECTION + 1] > MAX_WALL_DIST:
                    dc.forward(CURVE_SPEED)
                    steer_dir(-DIRECTION, 0.5)
                    sleep(0.2)
                    break
                if sensor_data[-DIRECTION + 1] < MIN_WALL_DIST:
                    dc.forward(CURVE_SPEED)
                    steer_dir(DIRECTION, 0.5)
                    sleep(0.2)
                    break
                dc.forward(SPEED)
                steer_dir(0)
                sleep(0.2)

finally:
    dc.stop_and_exit()
    servo.stop_and_exit()
