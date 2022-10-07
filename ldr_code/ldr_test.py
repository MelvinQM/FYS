import odroid_wiringpi as wpi
import time

LDR_PIN = 9
# verbind + met pin 1 (3.3 Volt)
# verbind - met pin 5 ground (0 Volt)
# verbind S met pin 6 (ALT1 Output)
LASER_PIN = 12

wpi.wiringPiSetup()

wpi.pinMode(LDR_PIN, wpi.INPUT)
wpi.pinMode(LASER_PIN, wpi.OUTPUT)
output = 0
outputOld = 0



# def gpio_callback():
#    print ("GPIO_CALLBACK!")

wpi.digitalWrite(LASER_PIN, wpi.HIGH)

while True:
    # Varuiabele
    output = wpi.digitalRead(LDR_PIN)
    # print(output, outputOld)
    if output > outputOld:
        print("Lichtje Uit")
    elif output < outputOld:
        print("Lichtje Aan")

    outputOld = output
    time.sleep(0.05)
