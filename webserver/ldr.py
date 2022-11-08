import odroid_wiringpi as wpi
import time


def ldr_func():

    LDR_PIN = 9
    # verbind + met pin 1 (3.3 Volt)
    # verbind - met pin 5 ground (0 Volt)
    # verbind S met pin 6 (ALT1 Output)
    LASER_PIN = 12

    wpi.wiringPiSetup()

    wpi.pinMode(LDR_PIN, wpi.INPUT)
    #return wpi.digitalRead(LDR_PIN)

    while True:

        # Varuiabele

        output = wpi.digitalRead(LDR_PIN)
        """
        # print(output, outputOld)
        if output > outputOld:
            print("Lichtje Uit")
        elif output < outputOld:
            print("Lichtje Aan")
        """
        outputOld = output
        print(output)
        time.sleep(0.5)

if __name__ == '__main__':
    ldr_func()