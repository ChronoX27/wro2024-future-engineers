import time
from picarx import Picarx
from robot_hat import Servo
from robot_hat.utils import reset_mcu

px = Picarx()

def reset():
    """Resettet alle Motoren."""
    print("Set servos to zero")
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    px.set_dir_servo_angle(0)
    reset_mcu()
    for i in range(12):
        Servo(i).angle(10)
        time.sleep(0.1)
        Servo(i).angle(0)
        time.sleep(0.1)

if __name__ == "__main__":
    reset()
