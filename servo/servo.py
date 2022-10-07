import random
import time

import odroid_wiringpi as wpi
from time import sleep

# zorgen dat de wpi pins worden gebruikt
wpi.wiringPiSetup()

# servo pin aanwijzen en instellen
servoPin = 1
wpi.pinMode(servoPin, wpi.PWM_OUTPUT)

# variabelen in steller voor het bewegen van de servo
delayTime = 0.1
minMove = 70
maxMove = 470

# loop met het bewegen van de servo
try:
    while True:
        move = random.randint(minMove, maxMove)
        wpi.pwmWrite(servoPin, move)
        time.sleep(delayTime)
        move = random.randint(minMove, maxMove)
        wpi.pwmWrite(servoPin, move)
        time.sleep(delayTime)

# zorgen dat de loop stopt bij 'ctrl c'
except KeyboardInterrupt:
    pass
# zorgen dat de servo weer naar het 0 punt beweegt
wpi.pwmWrite(servoPin, maxMove)
