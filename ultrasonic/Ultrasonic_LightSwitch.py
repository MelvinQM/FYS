# Libraries
import odroid_wiringpi as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.wiringPiSetup()

# set GPIO Pins
GPIO_TRIGGER = 7
GPIO_ECHO = 0
LED_PIN = 9

# set GPIO direction (IN / OUT)
GPIO.pinMode(GPIO_TRIGGER, GPIO.OUTPUT)
GPIO.pinMode(GPIO_ECHO, GPIO.INPUT)
GPIO.pinMode(LED_PIN, GPIO.OUTPUT)



def distance():
    # set Trigger to HIGH
    GPIO.digitalWrite(GPIO_TRIGGER, GPIO.HIGH)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.digitalWrite(GPIO_TRIGGER, GPIO.LOW)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.digitalRead(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.digitalRead(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if dist <= 100:
                GPIO.digitalWrite(LED_PIN, GPIO.HIGH)
            else:
                GPIO.digitalWrite(LED_PIN, GPIO.LOW)

            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)


        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")


