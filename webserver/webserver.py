# Importeren van alle python packages
from flask import Flask, render_template, request, redirect, jsonify
import sys
import odroid_wiringpi as wpi
import random
import time
import threading
import json
import mysql.connector
import spidev
import ws2812 as ws

# De pins aanwijzen en instellen
servoPin = 1
soundSensor_PIN = 29
LED_PIN = 0
LDR_PIN = 9
# set WPI Pins
triggerPin = 7
echoPin = 0

#SPI Poort
spi = spidev.SpiDev()
spi.open(0,0)

# Zorgen dat de wpi pins worden gebruikt
wpi.wiringPiSetup()

wpi.pinMode(servoPin, wpi.PWM_OUTPUT)
wpi.pinMode(LED_PIN, wpi.OUTPUT)
wpi.pinMode(LDR_PIN, wpi.INPUT)

# set WPI direction (IN / OUT)
wpi.pinMode(triggerPin, wpi.OUTPUT)
wpi.pinMode(echoPin, wpi.INPUT)

# Thresholds instellingen voor soundsensor
thresholdSound = 1700

# Game timer
gameCountdown = 0

# Delays
servoDelay = 0.5
soundDelay = 0.1
ldrDelay = 0.1
ultraSoundDelay = 0.001

#Kleuren
stoplichtBlauw = [[0,0,10],[0,0,0],[0,0,0],[0,0,0]]
stoplichtWit1 = [[0,0,0],[10,10,10],[0,0,0],[0,0,0]]
stoplichtRood = [[0,0,0],[0,0,0],[0,10,0],[0,0,0]]
stoplichtWit2 = [[10,10,10],[10,10,10],[10,10,10],[0,0,0]]

# Servo min en max in graden
minMove = 60
maxMove = 120
resetMove = 315

# Variabel initialiseren voor de functie
oldSound = 0
sound = 0
name_user = "  "
distance = 0


# Variabele voor het bijhouden van de score
score = 0
data = 0

# Main flask code stuk
app = Flask(__name__)

conn = mysql.connector.connect(host="localhost", user="admin", password="odroid123", database="FYS")


def databaseConn():
    if not conn.is_connected():
        mysql.connector.connect(host="localhost", user="admin", password="odroid123", database="FYS")


# Home Page
@app.route("/", methods=["GET", "POST"])
def home():
    testindex = "TEST INDEX"
    return render_template("index.html", testindex=testindex)


# Start de game loop
@app.route("/api")
def api():
    global data
    global gameCountdown
    wpi.wiringPiSetup()
    readldr = wpi.digitalRead(9)
    return jsonify({'score': score,
                    'timer': gameCountdown,
                    'waardeselect': data})


@app.route('/admin')
def databaseRead():
    with app.app_context():
        cursorRead = conn.cursor()
        cursorRead.execute("select * from Sound ORDER BY id DESC LIMIT 20")
        soundData = cursorRead.fetchall()  # data from database.
    return render_template("sensoren.html", value=soundData)


@app.route("/startgame", methods=["GET", "POST"])
def startgame():
    global gameCountdown
    global name_user
    global servoDelay
    global score
    global killTimer
    global oldSound

    # Resetting all the variables to starting values
    gameCountdown = 50
    servoDelay = 0.5
    score = 0
    killTimer = gameCountdown
    oldSound = 0

    name_user = request.form['name']
    return render_template("game.html", name_user=name_user)


@app.route("/gameover")
def gameover():
    with app.app_context():
        global conn
        # End program on 90
        wpi.pwmWrite(servoPin, resetMove)
        finalScore = score

        scoreInsert = conn.cursor()
        scoreInsert.execute("INSERT INTO Score (name, score) VALUES (%s, %s)", (name_user, finalScore))
        conn.commit()

        soundInsert = conn.cursor()
        soundInsert.execute("INSERT INTO Sound (sound) VALUES (%s)", ([oldSound]))
        conn.commit()

        scoreRead = conn.cursor()
        scoreRead.execute("select name, score from Score ORDER BY score DESC LIMIT 10")
        test = scoreRead.fetchall()  # data from database.
    return render_template("gameover.html", test=test, name_user=name_user, score=finalScore)


# Countdown for the gameloop
def countdown():
    global servoDelay
    global gameCountdown
    while True:
        while gameCountdown >= 0:
            time.sleep(1)
            gameCountdown -= 1
            # print(gameCountdown)
            # When the counter reaches the halfway point increase servo speed
            if gameCountdown == 60:
                servoDelay = 0.4


# Function for usage of Sound Sensor
def soundsensor():
    global oldSound
    while True:
        global sound
        # analogRead leest een float value van de sensor af (Geluid dus)
        sound = wpi.analogRead(soundSensor_PIN)
        time.sleep(soundDelay)
        if oldSound < sound:
            oldSound = sound
        # print(sound)

# Function for usage of servo
def servomovement():
    global gameCountdown
    global servoDelay
    # global killTimer
    killTimer = gameCountdown
    # Start program at 90 degrees
    wpi.pwmWrite(servoPin, resetMove)
    while True:
        while gameCountdown > 0:
            angle = random.randint(minMove, maxMove)
            move = ((angle / 18) + 2) * 45
            wpi.pwmWrite(servoPin, int(move))
            time.sleep(servoDelay)
            killTimer -= servoDelay


# Function for usage of ldr
def ldr_func():
    global LDR_PIN
    global score
    outputOld = 0
    while True:
        # Variabele
        output = wpi.digitalRead(9)
        # print(output)
        if output < outputOld:
            score = score + 1
        outputOld = output
        time.sleep(ldrDelay)


# Function for usage of ultrasonic
def ultrasonic():
    global distance
    try:
        while True:
            print("kaas")
            time.sleep(0.1)
            print("Measured distance: ",distance)
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
    except e:
        print(e)
        #return distance


def ultrasonicInsert():
    global distance
    with app.app_context():
        if __name__ == '__main__':
            while True:
                # print("Measured Distance = %.1f cm" % dist)
                time.sleep(1)

                cursor = conn.cursor()
                insert = "INSERT INTO Ultrasonic (data) VALUES (%s)"
                cursor.execute(insert, [distance])
                conn.commit()


def neopixelUltra():
    global distance
    while True:
        # dist is a variable made for distance()
        # dist = ultrasonic()

        # if statement that tells if distance is smaller than 100cm lights turn on
        if distance <= 100:
            ws.write2812(spi, stoplichtBlauw)
            time.sleep(0.1)
            ws.write2812(spi, stoplichtWit1)
            time.sleep(0.1)
            ws.write2812(spi, stoplichtRood)
            time.sleep(0.1)
        # else statements that tells if distance is larger than 100 cm light turn off
        else:
            ws.write2812(spi, stoplichtWit2)
            time.sleep(1)


def segmentDisplay():
    # fysieke pins: 13, 15, (36), 16, 29, 31, 33, 35
    SEGMENT_PINS = (2, 3, 27, 4, 21, 22, 23, 24)
    # fysieke pins 18, 22, 26, 32
    DIGIT_PINS = (5, 6, 11, 26)

    # Setup voor de pins van de segmenten
    for segment in SEGMENT_PINS:
        wpi.pinMode(segment, wpi.OUTPUT)
        wpi.digitalWrite(segment, 0)

    # Setup voor de pins van de 4 digits
    for digit in DIGIT_PINS:
        wpi.pinMode(digit, wpi.OUTPUT)
        wpi.digitalWrite(digit, 1)

    # Geeft aan welke pins aan gaan voor elk getal
    getalArray = {' ': (0, 0, 0, 0, 0, 0, 0, 0),
                  '0': (1, 1, 0, 1, 0, 1, 1, 1),
                  '1': (0, 0, 0, 1, 0, 1, 0, 0),
                  '2': (1, 1, 0, 0, 1, 1, 0, 1),
                  '3': (0, 1, 0, 1, 1, 1, 0, 1),
                  '4': (0, 0, 0, 1, 1, 1, 1, 0),
                  '5': (0, 1, 0, 1, 1, 0, 1, 1),
                  '6': (1, 1, 0, 1, 1, 0, 1, 1),
                  '7': (0, 0, 0, 1, 0, 1, 0, 1),
                  '8': (1, 1, 0, 1, 1, 1, 1, 1),
                  '9': (0, 1, 0, 1, 1, 1, 1, 1)}

    # het getal dat op de display moet staan, wordt ook een string zodat elk getal kan worden opgezocht in de array


    # Setup for the segments
    for segment in SEGMENT_PINS:
        wpi.pinMode(segment, wpi.OUTPUT)
        wpi.digitalWrite(segment, 0)

    # Setup for the 4 digits
    for digit in DIGIT_PINS:
        wpi.pinMode(digit, wpi.OUTPUT)
        wpi.digitalWrite(digit, 1)
    # het getal dat op de display moet staan, wordt ook een string zodat elk getal kan worden opgezocht in de array
    # de loop die de juiste pins aan zet voor elk getal op de display
    while True:
        getal = score * 100
        getalString = str(getal).rjust(4)
        for digit in range(4):
            for loop in range(0, 8):
                wpi.digitalWrite(SEGMENT_PINS[loop], getalArray[getalString[digit]][loop])
            # zet de juiste digit aan voor 0.001 seconde, zodat op elke digit een ander getal kan staan
            wpi.digitalWrite(DIGIT_PINS[digit], 0)
            time.sleep(0.001)
            wpi.digitalWrite(DIGIT_PINS[digit], 1)


# Making the threads
soundThread = threading.Thread(target=soundsensor)
databaseconnThread = threading.Thread(target=databaseConn)
ultraSonicThread = threading.Thread(target=ultrasonic)
insertThread = threading.Thread(target=ultrasonicInsert)
readThread = threading.Thread(target=databaseRead)
neopixelThread = threading.Thread(target=neopixelUltra)
servoThread = threading.Thread(target=servomovement)
countdownThread = threading.Thread(target=countdown)
segmentThread = threading.Thread(target=segmentDisplay)
ldrThread = threading.Thread(target=ldr_func)


if __name__ == '__main__':
    soundThread.start()
    ultraSonicThread.start()
    # insertThread.start()
    readThread.start()
    neopixelThread.start()
    # databaseconnThread.start()
    countdownThread.start()
    servoThread.start()
    ldrThread.start()
    segmentThread.start()

    app.run(host="0.0.0.0", port=80, debug=True)
