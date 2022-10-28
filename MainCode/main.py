## Project FYS
## This is the main code with all the sensors combined
## @author Koen, Melvin, Simon, Jayden
import random
import time
import odroid_wiringpi as wpi
#import sys
#from time import sleep

# Zorgen dat de wpi pins worden gebruikt
wpi.wiringPiSetup()

# Servo pin aanwijzen en instellen
servoPin = 1
wpi.pinMode(servoPin, wpi.PWM_OUTPUT)

# De pin van de sound sensor
soundSensor_PIN = 25
LED_PIN = 9
wpi.pinMode(LED_PIN, wpi.OUTPUT)

# Thresholds instellen voor soundsensor en Servo beweging
oldSound = 1460
minMove = 0
maxMove = 180

# Loop die zorgt voor functionaliteit servo en soundsensor
while True:
    # user input beweging optie
    # angle = float(input('Enter angle between 0 & 180: '))
    # move = ((angle/18)+2)*45
    move = random.randint(int((minMove/18)+2)*45, int((maxMove/18)+2)*45)
    wpi.pwmWrite(servoPin, int(move))
    time.sleep(0.5)
    try:
        # analogRead leest een float value van de sensor af (Geluid dus)
        sound = wpi.analogRead(soundSensor_PIN)
        print(sound)
        # Vergelijk het gelezen value met een preset value die je kan instellen bij oldSound
        if sound > oldSound:
            wpi.digitalWrite(LED_PIN, wpi.HIGH)
        else:
            wpi.digitalWrite(LED_PIN, wpi.LOW)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        wpi.digitalWrite(LED_PIN, wpi.LOW)
        print("Measurement stopped by User")
