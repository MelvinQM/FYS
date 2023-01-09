# Importeren van alle python packages
from flask import Flask, render_template, request, redirect, jsonify
import sys
import odroid_wiringpi as wpi
import random
import time
import threading
import json
import mysql.connector

conn = mysql.connector.connect(host="localhost", user="admin", password="odroid123", database="FYS")



if conn.is_connected():
    db_Info = conn.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
else:
    print("Connection failed to establish")

# Variabele voor het bijhouden van de score
score = 0

data = 0

# Main flask code stuk
app = Flask(__name__)

# Home Page
@app.route("/", methods=["GET", "POST"])
def home():
    testindex = "TEST INDEX"
    return render_template("index.html", testindex=testindex)


# Start de game loop
@app.route("/api")
def api():
    global data
    wpi.wiringPiSetup()
    readldr = wpi.digitalRead(9)
    return jsonify({'score': score,
                    'time': gameCountdown,
                    'waardeselect': data})


@app.route('/admin')
def databaseRead():
    with app.app_context():
        cursorRead = conn.cursor()
        cursorRead.execute("select * from Ultrasonic ORDER BY id DESC LIMIT 20")
        data = cursorRead.fetchall()  # data from database.
    return render_template("sensoren.html", value=data)



@app.route("/startgame", methods=["GET", "POST"])
def startgame():
    global name_user
    name_user = request.form['name']
    if ldrThread.is_alive() == False:
        ldrThread.start()
    countdownThread.start()
    return render_template("game.html", name_user=name_user)

@app.route("/gameover")
def gameover():
    finalScore = score
    name_user

    
    scoreInsert = conn.cursor()
    scoreData = "INSERT INTO Score (name, score) VALUES (%s, %s)"
    scoreInsert.execute(scoreData, [finalScore], [name_user])
    scoreInsert.commit()

    scoreRead = conn.cursor()
    scoreRead.execute("select name, score from Score ORDER BY score DESC LIMIT 10")
    test = scoreRead.fetchall()  # data from database.

    return render_template("gameover.html", test=test)

# De pins aanwijzen en instellen
servoPin = 1
soundSensor_PIN = 25
LED_PIN = 0
LDR_PIN = 9
# set WPI Pins
triggerPin = 7
echoPin = 0

# TODO Assign new pin to ultraLedStrip
# ultraLedStrip = 9

# Zorgen dat de wpi pins worden gebruikt
wpi.wiringPiSetup()

wpi.pinMode(servoPin, wpi.PWM_OUTPUT)
wpi.pinMode(LED_PIN, wpi.OUTPUT)
wpi.pinMode(LDR_PIN, wpi.INPUT)

# set WPI direction (IN / OUT)
wpi.pinMode(triggerPin, wpi.OUTPUT)
wpi.pinMode(echoPin, wpi.INPUT)
# wpi.pinMode(ultraLedStrip, wpi.OUTPUT)

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
minMove = 90
maxMove = 540
resetMove = 315

# Variabel initialiseren voor de functie
sound = 0
name_user = "  "

# Countdown for the gameloop
def countdown():
    global gameCountdown
    while gameCountdown:
        mins, secs = divmod(gameCountdown, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")
        time.sleep(1)
        gameCountdown -= 1
        # print(gameCountdown)

# Function for usage of Sound Sensor
def soundsensor():
    while True:
        global sound
        # analogRead leest een float value van de sensor af (Geluid dus)
        sound = wpi.analogRead(soundSensor_PIN)
        # ("Sound value:", sound)
        # Vergelijk het gelezen value met een preset value die je kan instellen bij oldSound
        if sound > thresholdSound:
            wpi.digitalWrite(LED_PIN, wpi.HIGH)
            # print("Threshold Exceeded")
        else:
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            # print("Below Threshold")
        time.sleep(soundDelay)

# Function for usage of servo
def servomovement():
    global gameCountdown
    killTimer = gameCountdown
    # Start program at 90 degrees
    wpi.pwmWrite(servoPin, resetMove)
    while killTimer > 0:
            move = random.randint(minMove, maxMove)
            wpi.pwmWrite(servoPin, int(move))
            time.sleep(servoDelay)
            killTimer -= 0.5
    # End program on 90
    wpi.pwmWrite(servoPin, resetMove)

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

        # print("Measured Distance = %.1f cm" % distance)
        time.sleep(1)

def databaseInsert():
    with app.app_context():
        if __name__ == '__main__':
            try:
                while True:
                    dist = distance()
                     #print("Measured Distance = %.1f cm" % dist)
                    time.sleep(1)
                    cursor = conn.cursor()

                    insert = "INSERT INTO Ultrasonic (data) VALUES (%s)"
                    cursor.execute(insert, [dist])
                    conn.commit()

                # Reset by pressing CTRL + C
            except KeyboardInterrupt:
                print("measurement stopped by user")

def databaseRead():
    with app.app_context():
        cursorRead = conn.cursor()
        cursorRead.execute("select * from Ultrasonic ORDER BY id DESC LIMIT 20")
        data = cursorRead.fetchall()  # data from database.
    return render_template("sensoren.html", value=data)


# Making the threads
countdownThread = threading.Thread(target=countdown)
soundThread = threading.Thread(target=soundsensor)
servoThread = threading.Thread(target=servomovement)
ldrThread = threading.Thread(target=ldr_func)
ultraSonicThread = threading.Thread(target=ultrasonic)
insertThread = threading.Thread(target=databaseInsert)
readThread = threading.Thread(target=databaseRead)

if __name__ == '__main__':
    soundThread.start()
    servoThread.start()
    ultraSonicThread.start()
    ldrThread.start()
    insertThread.start()
    readThread.start()
    app.run(host="0.0.0.0", port=80, debug=True)
