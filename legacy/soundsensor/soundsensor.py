import odroid_wiringpi as wpi
import time

wpi.wiringPiSetup()

# fysieke pin 40
SOUND_PIN = 29
soundLevel = 0

while 1:
    #leest analoge waarde van sound sensor
    soundLevel = wpi.analogRead(SOUND_PIN)

    #print algemeen geluidsniveau
    if soundLevel > 1500:
        print("Er is heel veel geluid!")
    elif soundLevel > 1300:
        print("Er is best veel geluid.")
    elif soundLevel > 1200:
        print("Er is wat geluid.")
    else:
        print("het is stil.")

    time.sleep(0.01)
