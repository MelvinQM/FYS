import odroid_wiringpi as wpi
import time

wpi.wiringPiSetup()
# physical pins 7, 11, 13, 15, 29, 31, 33, 35
SEGMENT_PINS = (7, 0, 2, 3, 21, 22, 23, 24)

# physical pins 12, 16, 18, 22
DIGIT_PINS = (6, 5, 4, 1)

# setup voor de pins van de segmenten
for segment in SEGMENT_PINS:
    wpi.pinMode(segment, wpi.OUTPUT)
    wpi.digitalWrite(segment, 0)

# setup voor de pins van de 4 digits
for digit in DIGIT_PINS:
    wpi.pinMode(digit, wpi.OUTPUT)
    wpi.digitalWrite(digit, 1)

# geeft aan welke pins aan gaan voor elk getal
getalArray = {' ': (0, 0, 0, 0, 0, 0, 0, 0),
              '0': (1, 1, 0, 1, 1, 1, 1, 0),
              '1': (0, 0, 0, 1, 0, 1, 0, 0),
              '2': (1, 1, 0, 0, 1, 1, 0, 1),
              '3': (0, 1, 0, 1, 1, 1, 0, 1),
              '4': (0, 0, 0, 1, 1, 1, 1, 0),
              '5': (0, 1, 0, 1, 1, 0, 1, 1),
              '6': (1, 1, 0, 1, 1, 0, 1, 1),
              '7': (0, 0, 0, 1, 0, 1, 0, 1),
              '8': (1, 1, 0, 1, 1, 1, 1, 1),
              '9': (0, 1, 0, 1, 1, 1, 1, 1)}

# het getal dat op de display moet staan, wordt ook een string zodat elk getal kan worden opgezocht in de array
getal = 1234
getalString = str(getal).rjust(4)

try:
    # de loop die de juiste pins aan zet voor elk getal op de display
    while True:
        for digit in range(4):
            for loop in range(0, 8):
                wpi.digitalWrite(SEGMENT_PINS[loop], getalArray[getalString[digit]][loop])
            # zet de juiste digit aan voor 0.001 seconde, zodat op elke digit een ander getal kan staan
            wpi.digitalWrite(DIGIT_PINS[digit], 0)
            time.sleep(0.001)
            wpi.digitalWrite(DIGIT_PINS[digit], 1)

except KeyboardInterrupt:
    wpi.ditigalWrite(SEGMENT_PINS, wpi.LOW)
