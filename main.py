from time import sleep
from picarx import Picarxööö  
# from vilib import Vilib
from robot_hat import Music, TTS


def reset():
    """Resettet alle Motoren."""
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    px.set_dir_servo_angle(0)


POWER = 10  # Geschwindigkeit des Robos beim Fahren.
LENKUNG = 35  # Einschlag des Lenkmotors
SAFE = 45  # Sagt dem Robo wie viel Sicherheitsabstand zu Objekten genug ist.
DANGER = 30  # Sagt dem Robo ab wie viel Abstand er sich sorgen machen muss. (Lenken)


def vor():
    px.forward(POWER)
    return "vor"


def zurück():
    px.backward(POWER)
    return "back"


def links():
    return "links"


def rechts():
    return "rechts"


def main():
    """Hauptschleife für den Roboter"""
    reset()

    try:
        last = ""
        while True:
            distance = round(px.ultrasonic.read())
            # Gerade aus fahren wenn sicht frei ist.
            if distance >= SAFE:
                # schützt vor endlos schleife
                if last == "back":
                    print("zurück > vor Abstand: " + str(distance))
                    px.set_dir_servo_angle(-LENKUNG)
                else:
                    px.set_dir_servo_angle(0)
                px.forward(POWER)
                last = "vor"
            # Wird gefährlich, Richtung ändern. (Wand oder Hinderniss zu nah)
            elif distance >= DANGER:
                px.set_dir_servo_angle(-LENKUNG)
                px.forward(POWER)

                last = "steuern"
            # Kein Ausweg mehr, Robo ist zu nah am Hindernis oder der Wand um zu fahren.
            else:
                # schützt vor endlos schleife
                if last == "vor":
                    print("vor > zurück Abstand: " + str(distance))
                    px.set_dir_servo_angle(LENKUNG)
                else:
                    px.set_dir_servo_angle(0)
                px.backward(POWER)

                last = "back"
            sleep(0.5)
    finally:
        px.forward(0)
        reset()


px = Picarx()

tts = TTS()
tts.lang("de-DE")
music = Music()
music.music_set_volume(10)

# für aufgabe 1 nicht benötigt
# Vilib.camera_start(vflip=False,hflip=False)
# Vilib.display(local=True,web=True)

if __name__ == "__main__":
    main()
