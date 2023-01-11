# Libraries
import odroid_wiringpi as wpi
import time
import spidev
import ws2812 as ws

# GPIO Mode (BOARD / BCM)
wpi.wiringPiSetup()

# set GPIO Pins
GPIO_TRIGGER = 7
GPIO_ECHO = 0
GPIO_CONN = 19

#SPI Poort
spi = spidev.SpiDev()
spi.open(0,0)


# set GPIO direction (IN / OUT)
wpi.pinMode(GPIO_TRIGGER, wpi.OUTPUT)
wpi.pinMode(GPIO_ECHO, wpi.INPUT)
# GPIO.pinMode(GPIO_CONN, GPIO.OUTPUT)

#Kleuren
stoplichtGroen = [[0,0,10],[0,0,0],[0,0,0],[0,0,0]]
stoplichtOranje = [[0,0,0],[10,10,10],[0,0,0],[0,0,0]]
stoplichtRood = [[0,0,0],[0,0,0],[0,10,0],[0,0,0]]
stoplichtWit = [[10,10,10],[10,10,10],[10,10,10],[0,0,0]]



def distance():
    # set Trigger to HIGH
    wpi.digitalWrite(GPIO_TRIGGER, wpi.HIGH)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    wpi.digitalWrite(GPIO_TRIGGER, wpi.LOW)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while wpi.digitalRead(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while wpi.digitalRead(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    if __name__ == '__main__':
        while True:
            # dist is a variable made for distance()
            dist = distance()
            # if statement that tells if distance is smaller than 100cm lights turn on
            if dist <= 100:
                ws.write2812(spi, stoplichtGroen)
                time.sleep(0.1)
                ws.write2812(spi, stoplichtOranje)
                time.sleep(0.1)
                ws.write2812(spi, stoplichtRood)
            # else statements that tells if distance is larger than 100 cm light turn off
            else:
                ws.write2812(spi, stoplichtWit)

            print("Measured Distance = %.1f cm" % dist)

    return distance


# if __name__ == '__main__':
#     while True:
#         # dist is a variable made for distance()
#         dist = distance()
#         # if statement that tells if distance is smaller than 100cm lights turn on
#         if dist <= 100:
#             ws.write2812(spi, stoplichtGroen)
#             time.sleep(0.1)
#             ws.write2812(spi, stoplichtOranje)
#             time.sleep(0.1)
#             ws.write2812(spi, stoplichtRood)
#             time.sleep(0.1)
#         # else statements that tells if distance is larger than 100 cm light turn off
#         else:
#             ws.write2812(spi, stoplichtWit)


