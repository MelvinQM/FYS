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
wpi.pinMode(servoPin, wpi.PWM_OUTPUT)

# De pin van de sound sensor
soundSensor_PIN = 25 # Physical 37
LED_PIN = 9
LDR_PIN = 3
wpi.pinMode(LED_PIN, wpi.OUTPUT)

# Thresholds instellen voor soundsensor en Servo beweging
thresholdSound = 1700
servoDelay = 0.5
soundDelay = 0.1
ldrDelay = 0.1
minMove = 0
maxMove = 180

# Variabel initialiseren voor de functie
sound = 0

wpi.pinMode(LDR_PIN, wpi.INPUT)
#wpi.pinMode(LASER_PIN, wpi.OUTPUT)

# Function for usage of Sound Sensor
def soundSensor():
    while True:
        global sound
        # analogRead leest een float value van de sensor af (Geluid dus)
        sound = wpi.analogRead(soundSensor_PIN)
        print("Sound value:", sound)
        # Vergelijk het gelezen value met een preset value die je kan instellen bij oldSound
        if sound > thresholdSound:
            wpi.digitalWrite(LED_PIN, wpi.HIGH)
            print("Threshold Exceeded")
        else:
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            print("Below Threshold")
        time.sleep(soundDelay)


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


def ldr_func():
    while True:
        # Variabele
        output = wpi.digitalRead(3)
        """
        outputOld = 0
        # print(output, outputOld)
        if output > outputOld:
            print("Lichtje Uit")
        elif output < outputOld:
            print("Lichtje Aan")
        """
        print(output)
        outputOld = output
        time.sleep(ldrDelay)

# Thread aangemaakt
soundThread = threading.Thread(target=soundSensor)
servoThread = threading.Thread(target=servoMovement)
ldrThread = threading.Thread(target=ldr_func)

# Start threading
soundThread.start()
servoThread.start()
ldrThread.start()

