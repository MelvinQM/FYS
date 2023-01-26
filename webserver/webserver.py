# Importeren van alle python packages
from flask import Flask, render_template, request, redirect, jsonify
import sys
import odroid_wiringpi as wpi
import random
import time
import threading
import mysql.connector
import spidev
import ws2812 as ws

# De pins aanwijzen en instellen
servoPin = 1
soundPin = 29
ldrPin = 9
triggerPin = 7
echoPin = 0

# SPI Poort
spi = spidev.SpiDev()
spi.open(0,0)

wpi.wiringPiSetup()

wpi.pinMode(servoPin, wpi.PWM_OUTPUT)
wpi.pinMode(ldrPin, wpi.INPUT)

# Set WPI direction (IN / OUT)
wpi.pinMode(triggerPin, wpi.OUTPUT)
wpi.pinMode(echoPin, wpi.INPUT)

# Thresholds settings for the soundsensor
thresholdSound = 1700

# Game timer
gameCountdown = 0

# Delays
servoDelay = 0.5
soundDelay = 0.1
ldrDelay = 0.1
ultraSoundDelay = 0.1

# Colors
stoplichtBlauw = [[0,0,10],[0,0,0],[0,0,0],[0,0,0]]
stoplichtWit1 = [[0,0,0],[10,10,10],[0,0,0],[0,0,0]]
stoplichtRood = [[0,0,0],[0,0,0],[0,10,0],[0,0,0]]
stoplichtWit2 = [[10,10,10],[10,10,10],[10,10,10],[0,0,0]]

# Servo min and max in degrees
minMove = 60
maxMove = 120
resetMove = 315

# Variabels initialized for function usage
oldSound = 0
sound = 0
nameUser = "  "
distance = 0


# Variabel for keeping track of the score
score = 0
data = 0

# Initialize flask app and connect to the database on oege
app = Flask(__name__)
conn = mysql.connector.connect(host="oege.ie.hva.nl", user="moesmq", password="P3$JQTmF#Vr2WH", database="zmoesmq")

# Function that checks if the database is connected if not connect again
def databaseConn():
    global conn
    if not conn.is_connected():
       conn = mysql.connector.connect(host="oege.ie.hva.nl", user="moesmq", password="P3$JQTmF#Vr2WH", database="zmoesmq")


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
    return jsonify({'score': score,
                    'timer': gameCountdown,
                    'waardeselect': data})


# Function that created a cursor that is used to fetch the values of sound using a select query.
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
    global nameUser
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

    nameUser = request.form['name']
    return render_template("game.html", nameUser=nameUser)


@app.route("/gameover")
def gameover():
    with app.app_context():
        global conn
        # End program on 90
        wpi.pwmWrite(servoPin, resetMove)
        finalScore = score

        scoreInsert = conn.cursor()
        scoreInsert.execute("INSERT INTO Score (name, score) VALUES (%s, %s)", (nameUser, finalScore))
        conn.commit()

        soundInsert = conn.cursor()
        soundInsert.execute("INSERT INTO Sound (sound) VALUES (%s)", ([oldSound]))
        conn.commit()

        # Fetching values from database to display in the leaderboard
        scoreRead = conn.cursor()
        scoreRead.execute("select name, score from Score ORDER BY score DESC LIMIT 10")
        test = scoreRead.fetchall()  # data from database.
    return render_template("gameover.html", test=test, nameUser=nameUser, score=finalScore)


# Countdown for the gameloop
def countdown():
    global servoDelay
    global gameCountdown
    while True:
        while gameCountdown >= 0:
            time.sleep(1)
            gameCountdown -= 1

            # When the counter reaches the halfway point increase servo speed
            if gameCountdown == 60:
                servoDelay = 0.4


# Function for usage of Sound Sensor
def soundsensor():
    global oldSound
    while True:
        global sound
        # analogRead leest een float value van de sensor af (Geluid dus)
        sound = wpi.analogRead(soundPin)
        time.sleep(soundDelay)
        if oldSound < sound:
            oldSound = sound


# Function for usage of servo
def servomovement():
    global gameCountdown
    global servoDelay
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
    global ldrPin
    global score
    outputOld = 0
    while True:
        output = wpi.digitalRead(ldrPin)
        if output < outputOld:
            score = score + 1
        outputOld = output
        time.sleep(ldrDelay)


# Function for usage of ultrasonic
def ultrasonic():
    global distance
    try:
        while True:
            time.sleep(ultraSoundDelay)

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

            # Time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # Multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
    except:
        print("Ultrasonic is not functioning properly")



def ultrasonicInsert():
    global distance
    with app.app_context():
        if __name__ == '__main__':
            while True:
                time.sleep(1)

                cursor = conn.cursor()
                insert = "INSERT INTO Ultrasonic (data) VALUES (%s)"
                cursor.execute(insert, [distance])
                conn.commit()


def neopixelUltra():
    global distance
    while True:
        # If statement that tells if distance is smaller than 100cm lights turn on
        if distance <= 100:
            ws.write2812(spi, stoplichtBlauw)
            time.sleep(ultraSoundDelay)
            ws.write2812(spi, stoplichtWit1)
            time.sleep(ultraSoundDelay)
            ws.write2812(spi, stoplichtRood)
            time.sleep(ultraSoundDelay)
        # Else statements that tells if distance is larger than 100 cm light turn off
        else:
            ws.write2812(spi, stoplichtWit2)
            time.sleep(1)


def segmentDisplay():
    # Physical pins: 13, 15, (36), 16, 29, 31, 33, 35
    segmentPins = (2, 3, 27, 4, 21, 22, 23, 24)
    # Physical pins 18, 22, 26, 32
    digitPins = (5, 6, 11, 26)

    # Setup for the pins for the segments
    for segment in segmentPins:
        wpi.pinMode(segment, wpi.OUTPUT)
        wpi.digitalWrite(segment, 0)

    # Setup for the pins of the 4 digits
    for digit in digitPins:
        wpi.pinMode(digit, wpi.OUTPUT)
        wpi.digitalWrite(digit, 1)

    # Determines which leds turn on for every respective number
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

    # Setup for the segments
    for segment in segmentPins:
        wpi.pinMode(segment, wpi.OUTPUT)
        wpi.digitalWrite(segment, 0)

    # Setup for the 4 digits
    for digit in digitPins:
        wpi.pinMode(digit, wpi.OUTPUT)
        wpi.digitalWrite(digit, 1)

    # The loop that turns on the right pins for each number on the display
    while True:
        getal = score * 100
        getalString = str(getal).rjust(4)
        for digit in range(4):
            for loop in range(0, 8):
                wpi.digitalWrite(segmentPins[loop], getalArray[getalString[digit]][loop])
            # Turn on the right digit for 0.001 seconds, so that on every digit there can be a different number
            wpi.digitalWrite(digitPins[digit], 0)
            time.sleep(0.001)
            wpi.digitalWrite(digitPins[digit], 1)


# Making the threads
soundThread = threading.Thread(target=soundsensor)
databaseconnThread = threading.Thread(target=databaseConn)
ultraSonicThread = threading.Thread(target=ultrasonic)
# insertThread = threading.Thread(target=ultrasonicInsert)
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
    databaseconnThread.start()
    countdownThread.start()
    servoThread.start()
    ldrThread.start()
    segmentThread.start()

    app.run(host="0.0.0.0", port=80, debug=True)
