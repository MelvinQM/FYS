import odroid_wiringpi as wpi
import time

wpi.wiringPiSetup()
# physical pins 7, 11, 12, 13, 15, 16, 26, 29
SEGMENT_PINS = (7, 0, 1, 2, 3, 4, 11, 21)
# TEST_PIN = 7


for segment in SEGMENT_PINS:
    wpi.pinMode(segment, wpi.OUTPUT)
    wpi.digitalWrite(segment, wpi.LOW)
