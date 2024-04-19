from time import sleep
from picarx import Picarx
from vilib import Vilib
from robot_hat import Music,TTS

def reset():
    """Resettet alle Motoren."""
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    px.set_dir_servo_angle(0)

# def detect_colors(): # Soll Orte und Farben von Hindernissen finden.
#     print("Hier kommt mal code hin")

def main():
    """Hauptschleife für den Roboter"""
    reset()

    POWER = 5 # Geschwindigkeit des Robos beim Fahren.
    LENKUNG = 30 # Einschlag des Lenkmotors
    SAFE = 35 # Sagt dem Robo wie viel Sicherheitsabstand zu Objekten genug ist.
    DANGER = 20 # Sagt dem Robo ab wie viel Abstand er sich sorgen machen muss. (Lenken)

    try:
        while True:
            distance = round(px.ultrasonic.read())
            # Gerade aus fahren wenn sicht frei ist.
            if distance >= SAFE:
                px.set_dir_servo_angle(0)
                px.forward(POWER)
            # Wird gefährlich, richtung ändern. (Wand oder Hinderniss zu nah)
            elif distance >= DANGER:
                px.set_dir_servo_angle(-LENKUNG)
                px.forward(POWER)
                sleep(.5)
            # Kein Ausweg mehr, Robo ist zu nah am Hinderniss oder der Wand um zu fahren.
            else: 
                px.set_dir_servo_angle(0)
                px.backward(POWER)
                sleep(.5)
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
