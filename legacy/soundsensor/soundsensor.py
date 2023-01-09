import odroid_wiringpi as wpi
import time

wpi.wiringPiSetup()

# fysieke pin 40
SOUND_PIN = 29
soundLevel = 0

# wpi.pinMode(SOUND_PIN, wpi.INPUT)

while 1:
    print(wpi.analogRead(SOUND_PIN))
    time.sleep(0.1)

