import odroid_wiringpi as wpi
import time

LDR_PIN = 9
# + op pin 1 (3.3v)
# - op pin 5 (ground)
# S op pin 6 (ALT1 output)
LASER_PIN = 12

LDR_DELAY = 0.01

wpi.wiringPiSetup()

wpi.pinMode(LASER_PIN, wpi.OUTPUT)
wpi.pinMode(LDR_PIN, wpi.INPUT)

score = 0
output = 0
outputOld = 0

wpi.digitalWrite(LASER_PIN, wpi.HIGH)

while True:
    try:
        output = wpi.digitalRead(LDR_PIN)
        if output > outputOld:
            print("Lichtje Uit")
            score = score + 1
        elif output < outputOld:
            print("Lichtje Aan")
        # print(output)
        outputOld = output
        time.sleep(LDR_DELAY)

    except KeyboardInterrupt:
        wpi.ditigalWrite(LASER_PIN, wpi.LOW)
        print("Score " + score)
