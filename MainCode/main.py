## Project FYS
## This is the main code with all the sensors combined
## @author Koen, Melvin, Simon, Jayden
import random
import time
import threading
import logging
import odroid_wiringpi as wpi

# Zorgen dat de wpi pins worden gebruikt
wpi.wiringPiSetup()

# Servo pin aanwijzen en instellen
servoPin = 1
servoDelay = 0.5
wpi.pinMode(servoPin, wpi.PWM_OUTPUT)

# De pin van de sound sensor
soundSensor_PIN = 37
LED_PIN = 9
wpi.pinMode(LED_PIN, wpi.OUTPUT)

# Thresholds instellen voor soundsensor en Servo beweging
oldSound = 1460
minMove = 0
maxMove = 180
sound = 0

# Function for usage of Sound Sensor
def soundSensor():
    while True:
        global sound
        # analogRead leest een float value van de sensor af (Geluid dus)
        sound = wpi.analogRead(soundSensor_PIN)
        print(sound)
        # Vergelijk het gelezen value met een preset value die je kan instellen bij oldSound
        if sound > oldSound:
            wpi.digitalWrite(LED_PIN, wpi.HIGH)
            print("wpi.HIGH")
        else:
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            print("wpi.LOW")



def servoMovement():
    while True:
        try:
            # user input beweging optie
            # angle = float(input('Enter angle between 0 & 180: '))
            # move = ((angle/18)+2)*45
            move = random.randint(int((minMove / 18) + 2) * 45, int((maxMove / 18) + 2) * 45)
            wpi.pwmWrite(servoPin, int(move))
            time.sleep(servoDelay)

        except KeyboardInterrupt:
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            print("Measurement stopped by User")


# Thread aangemaakt
soundThread = threading.Thread(target=soundSensor)
servoThread = threading.Thread(target=servoMovement)
# Start threading
soundThread.start()
servoThread.start()



""" 
# Loop die zorgt voor functionaliteit servo en soundsensor
while True:
    try:
        # user input beweging optie
        # angle = float(input('Enter angle between 0 & 180: '))
        # move = ((angle/18)+2)*45
        move = random.randint(int((minMove / 18) + 2) * 45, int((maxMove / 18) + 2) * 45)
        wpi.pwmWrite(servoPin, int(move))
        time.sleep(0.5)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        wpi.digitalWrite(LED_PIN, wpi.LOW)
        print("Measurement stopped by User")
"""

