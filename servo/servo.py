import odroid_wiringpi as wpi
import random
import time

# Setup
servoPin = 1

wpi.wiringPiSetup()
wpi.pinMode(servoPin, wpi.PWM_OUTPUT)

gameCountdown = 120
servoDelay = 0.5
# Servo min en max
minMove = 90
maxMove = 540
resetMove = 315


def servomovement():
    global gameCountdown
    oldMove = 90
    killTimer = gameCountdown
    # Start program at 90 degrees
    wpi.pwmWrite(servoPin, resetMove)
    while killTimer > 0:
        move = random.randint(minMove, maxMove)
        wpi.pwmWrite(servoPin, move)
        time.sleep(servoDelay)
        print(move)
        killTimer -= 0.5
    # End program on 90
    wpi.pwmWrite(servoPin, resetMove)
servomovement()