from time import sleep
from picarx import Picarx
from vilib import Vilib
from robot_hat import Music,TTS

def reset(): # Resettet alle Motoren.
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    px.set_dir_servo_angle(0)

px = Picarx()

tts = TTS()
tts.lang("de-DE")
music = Music()
music.music_set_volume(10)

reset()

Vilib.camera_start(vflip=False,hflip=False)
Vilib.display(local=True,web=True)

POWER = 5 # Geschwindigkeit des Robos beim Fahren.
SafeDistance = 40 # Sagt dem Robo wie viel Sicherheitsabstand zu Objekten genug ist.
DangerDistance = 30 # Sagt dem Robo ab wie viel Abstand er sich sorgen machen muss. (Lenken)

def main():
    try:
        while True:
            distance = round(px.ultrasonic.read(), 2)
            if distance >= SafeDistance: # Gerade aus fahren wenn sicht frei ist.
                px.set_dir_servo_angle(0)
                px.forward(POWER)
            elif distance >= DangerDistance: # Wird gefährlich, richtung ändern. (Wand oder Hinderniss zu nah)
                px.set_dir_servo_angle(-25)
                px.forward(POWER)
                sleep(.5)
            else: # Kein Ausweg mehr, Robo ist zu nah am Hinderniss oder der Wand um zu fahren.
                px.set_dir_servo_angle(25)
                px.forward(1)
                sleep(.5)
    finally:
        px.forward(0)
        reset()

def detect_colors(): # Soll Orte und Farben von Hindernissen finden.
    print("Hier kommt mal code hin")

if __name__ == "__main__":
    main()