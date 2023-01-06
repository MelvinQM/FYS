import odroid_wiringpi as wpi
import time

# De pin van de sound sensor
soundSensor_PIN = 25
LED_PIN = 9
wpi.wiringPiSetup()
#wpi.pinMode(soundSensor_PIN, wpi.INPUT)
wpi.pinMode(LED_PIN, wpi.OUTPUT)

oldSound = 1460
while True:
    time.sleep(0.01)
    try:
        sound = wpi.analogRead(soundSensor_PIN)
        print(sound)
        if sound > oldSound:
            wpi.digitalWrite(LED_PIN, wpi.HIGH)
            #print("Aan")
        else:
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            #print("Uit")

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        wpi.digitalWrite(LED_PIN, wpi.LOW)
        print("Measurement stopped by User")


