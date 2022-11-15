## Project FYS
## This is the main code with all the sensors combined
## @author Koen, Melvin, Simon, Jayden
import random
import time
import threading
import odroid_wiringpi as wpi

# Zorgen dat de wpi pins worden gebruikt
wpi.wiringPiSetup()

# De pins aanwijzen en instellen
servoPin = 1
soundSensor_PIN = 25
LED_PIN = 9
LDR_PIN = 24
wpi.pinMode(servoPin, wpi.PWM_OUTPUT)
wpi.pinMode(LED_PIN, wpi.OUTPUT)
wpi.pinMode(LDR_PIN, wpi.INPUT)

# set WPI Pins
triggerPin = 7
echoPin = 0
ultraLedStrip = 9


# set WPI direction (IN / OUT)
wpi.pinMode(triggerPin, wpi.OUTPUT)
wpi.pinMode(echoPin, wpi.INPUT)
wpi.pinMode(ultraLedStrip, wpi.OUTPUT)

# Thresholds instellingen voor soundsensor
thresholdSound = 1700

# Game timer
gameCountdown = 120

# Delays
servoDelay = 0.5
soundDelay = 0.1
ldrDelay = 0.1
ultraSoundDelay = 0.00001

# Servo min en max
minMove = 0
maxMove = 180

# Variabel initialiseren voor de functie
sound = 0

# wpi.pinMode(LASER_PIN, wpi.OUTPUT)

# Countdown for the gameloop
def countdown():
    global gameCountdown
    while gameCountdown:
        mins, secs = divmod(gameCountdown, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        gameCountdown -= 1
        print(timer)

# Function for usage of Sound Sensor
def soundsensor():
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

# Function for usage of servo
def servomovement():
    global gameCountdown
    killTimer = gameCountdown
    while killTimer > 0:
        try:
            # user input beweging optie
            # angle = float(input('Enter angle between 0 & 180: '))
            # move = ((angle/18)+2)*45
            move = random.randint(int((minMove / 18) + 2) * 45, int((maxMove / 18) + 2) * 45)
            wpi.pwmWrite(servoPin, int(move))
            time.sleep(servoDelay)
            killTimer -= 0.5

        except KeyboardInterrupt:
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            print("Measurement stopped by User")

# Function for usage of ldr
def ldr_func():
    while True:
        global LDR_PIN
        # Variabele
        output = wpi.digitalRead(LDR_PIN)
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

# Function for usage of ultrasonic
def ultrasonic():
    while True:
        # dist is a variable made for distance()
        # set Trigger to HIGH
        wpi.digitalWrite(triggerPin, wpi.HIGH)

        # set Trigger after 0.01ms to LOW
        time.sleep(ultraSoundDelay)
        wpi.digitalWrite(triggerPin, wpi.LOW)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while wpi.digitalRead(echoPin) == 0:
            StartTime = time.time()

        # save time of arrival
        while wpi.digitalRead(echoPin) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        # if statement that tells if distance is smaller than 100cm lights turn on
        if distance <= 100:
            wpi.digitalWrite(ultraLedStrip, wpi.HIGH)
        # else statements that tells if distance is larger than 100 cm light turn off
        else:
            wpi.digitalWrite(ultraLedStrip, wpi.LOW)

        print("Measured Distance = %.1f cm" % distance)
        time.sleep(1)


# Making the threads
countdownThread = threading.Thread(target=countdown)
soundThread = threading.Thread(target=soundsensor)
servoThread = threading.Thread(target=servomovement)
ldrThread = threading.Thread(target=ldr_func)
ultraSonicThread = threading.Thread(target=ultrasonic)

# Starting the threading
countdownThread.start()
soundThread.start()
servoThread.start()
ldrThread.start()
ultraSonicThread.start()



