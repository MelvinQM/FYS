import odroid_wiringpi as wpi
import time

wpi.wiringPiSetup()
# physical pins 7, 11, 13, 15, 29, 31, 32, 35
SEGMENT_PINS = (7, 0, 2, 3, 21, 22, 23, 24)

# physical pins 12, 16, 18, 22
DIGIT_PINS = (1, 4, 5, 6)

for segment in SEGMENT_PINS:
    wpi.pinMode(segment, wpi.OUTPUT)
    wpi.digitalWrite(segment, 0)



number = {' ': (0, 0, 0, 0, 0, 0, 0),
          '0': (1, 1, 1, 1, 1, 1, 0),
          '1': (0, 1, 1, 0, 0, 0, 0),
          '2': (1, 1, 0, 1, 1, 0, 1),
          '3': (1, 1, 1, 1, 0, 0, 1),
          '4': (0, 1, 1, 0, 0, 1, 1),
          '5': (1, 0, 1, 1, 0, 1, 1),
          '6': (1, 0, 1, 1, 1, 1, 1),
          '7': (1, 1, 1, 0, 0, 0, 0),
          '8': (1, 1, 1, 1, 1, 1, 1),
          '9': (1, 1, 1, 1, 0, 1, 1)}

try:
    while True:
        n = time.ctime()[11:13] + time.ctime()[14:16]
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0, 7):
                wpi.digitalWrite(SEGMENT_PINS[loop], number[s[digit]][loop])
                if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                    wpi.digitalWrite(25, 1)
                else:
                    wpi.digitalWrite(25, 0)
            wpi.digitalWrite(digits[digit], 0)
            time.sleep(0.001)
            wpi.digitalWrite(digits[digit], 1)

    except KeyboardInterrupt:
        wpi.ditigalWrite(SEGMENT_PINS, wpi.LOW)

for segment in SEGMENT_PINS:
    wpi.pinMode(segment, wpi.OUTPUT)
    wpi.digitalWrite(segment, wpi.HIGH)
