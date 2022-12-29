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
minMove = 0
maxMove = 180
resetMove = 315


def servomovement():
    global gameCountdown
    oldMove = 90
    killTimer = gameCountdown
    # Start program at 90 degrees
    wpi.pwmWrite(servoPin, resetMove)
    time.sleep(1)
    while killTimer > 0:
        move = random.randint(int((minMove / 18) + 2) * 45, int((maxMove / 18) + 2) * 45)
        wpi.pwmWrite(servoPin, move)
        time.sleep(servoDelay)
        print(move)
        killTimer -= 0.5
    # End program on 90
    wpi.pwmWrite(servoPin, resetMove)
servomovement()