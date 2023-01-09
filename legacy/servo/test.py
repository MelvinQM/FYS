import random
import time

import odroid_wiringpi as wpi
from time import sleep

#zorgen dat de wpi pins worden gebruikt
wpi.wiringPiSetup()

#servo pin aanwijzen en instellen
servoPin = 1
wpi.pinMode(servoPin, wpi.PWM_OUTPUT)

#loop met het bewegen van de servo
while True:
    angle = float(input('Enter angle between 0 & 180: '))
    move = ((angle/18)+2)*45
    wpi.pwmWrite(servoPin, int(move))
    time.sleep(0.5)
