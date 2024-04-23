import time
from picarx import Picarx
from robot_hat import Servo
from robot_hat.utils import reset_mcu


def reset(px):
    """Resettet alle Motoren."""
    print("Set servos to zero")
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    px.set_dir_servo_angle(0)
    reset_mcu()
    for i in range(12):
        Servo(i).angle(15)
        time.sleep(0.1)
        Servo(i).angle(-15)
        time.sleep(0.1)
        Servo(i).angle(0)

    # px.left_rear_dir_pin.off()
    # px.right_rear_dir_pin.off()


if __name__ == "__main__":
    px = Picarx()
    reset(px)
