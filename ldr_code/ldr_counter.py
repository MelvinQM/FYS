import time
import odroid_wiringpi as wpi

# LDR_PIN = 3
# LDR_DELAY = 0.1

wpi.pinMode(3, wpi.INPUT)
outputOld = 0

while True:
    output = wpi.digitalRead(LDR_PIN)
    if output > outputOld:
        print("Lichtje Uit")
    elif output < outputOld:
        print("Lichtje Aan")
    print(output)
    outputOld = output
    time.sleep(0.1)
