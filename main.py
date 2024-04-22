from time import sleep
from picarx import Picarx

# from vilib import Vilib
# from robot_hat import Music, TTS

px = Picarx()
POWER = 50  # Geschwindigkeit des Robos beim Fahren.
LENKUNG = 30  # Einschlag des Lenkmotors
SAFE = 40  # Sagt dem Robo wie viel Sicherheitsabstand zu Objekten genug ist.
DANGER = 20  # Sagt dem Robo ab wie viel Abstand er sich sorgen machen muss. (Lenken)

# POWER = 50
# SafeDistance = 40   # > 40 safe
# DangerDistance = 20 # > 20 && < 40 turn around,
#                     # < 20 backward


def reset():
    """Resettet alle Motoren."""
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    px.set_dir_servo_angle(0)


def main():
    """Hauptschleife für den Roboter"""
    reset()

    # last = ""
    while True:
        distance = round(px.ultrasonic.read())
        # Gerade aus fahren wenn sicht frei ist.
        if distance >= SAFE:
            # schützt vor endlos schleife
            # if last == "back":
            #     print("zurück > vor Abstand: " + str(distance))
            #     px.set_dir_servo_angle(-LENKUNG)
            # else:
            #     px.set_dir_servo_angle(0)
            px.set_dir_servo_angle(0)
            px.forward(POWER)
        # last = "vor"
        # Wird gefährlich, Richtung ändern. (Wand oder Hinderniss zu nah)
        elif distance >= DANGER:
            print("lenkmanöver")
            # px.set_dir_servo_angle(LENKUNG)
            # px.backward(POWER)
            # px.set_dir_servo_angle(-LENKUNG)
            # px.forward(POWER)
            # sleep(0.1)
            px.set_dir_servo_angle(LENKUNG)
            px.forward(POWER)
            sleep(0.1)

            # last = "steuern"
        # Kein Ausweg mehr, Robo ist zu nah am Hindernis oder der Wand um zu fahren.
        else:
            print("zurück")
            # # schützt vor endlos schleife (vielleicht)
            # if last == "vor":
            #     print("vor > zurück Abstand: " + str(distance))
            #     px.set_dir_servo_angle(LENKUNG)
            # else:
            #     px.set_dir_servo_angle(0)
            px.set_dir_servo_angle(-LENKUNG)
            px.backward(POWER)
            sleep(0.5)
            # last = "back"





# tts = TTS()
# tts.lang("de-DE")
# music = Music()
# music.music_set_volume(10)

# Für Aufgabe 1 nicht benötigt
# Vilib.camera_start(vflip=False,hflip=False)
# Vilib.display(local=True,web=True)

# px = Picarx()

if __name__ == "__main__":
    main()
