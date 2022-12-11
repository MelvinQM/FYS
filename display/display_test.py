import odroid_wiringpi as wpi
import time

wpi.wiringPiSetup()
# physical pins 7, 11, 13, 15, 29, 31, 33, 35
SEGMENT_PINS = (7, 0, 2, 3, 21, 22, 23, 24)

# physical pins 12, 16, 18, 22
DIGIT_PINS = (6, 5, 4, 1)

for segment in SEGMENT_PINS:
    wpi.pinMode(segment, wpi.OUTPUT)
    wpi.digitalWrite(segment, 0)

for digit in DIGIT_PINS:
    wpi.pinMode(digit, wpi.OUTPUT)
    wpi.digitalWrite(digit, 1)

number = {' ': (0, 0, 0, 0, 0, 0, 0, 0),
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

try:
    while True:
        n = 1234
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0, 8):
                wpi.digitalWrite(SEGMENT_PINS[loop], number[s[digit]][loop])

            wpi.digitalWrite(DIGIT_PINS[digit], 0)
            time.sleep(0.001)
            wpi.digitalWrite(DIGIT_PINS[digit], 1)

except KeyboardInterrupt:
    wpi.ditigalWrite(SEGMENT_PINS, wpi.LOW)
