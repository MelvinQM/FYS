import threading

from flask import Flask, render_template
import odroid_wiringpi as wpi
import time


import mysql.connector

wpi.wiringPiSetup()

# set WPI Pins
triggerPin = 7
echoPin = 0

wpi.pinMode(triggerPin, wpi.OUTPUT)
wpi.pinMode(echoPin, wpi.INPUT)

ultraSoundDelay = 0.00001

# Main flask code stuk
app = Flask(__name__)

conn = mysql.connector.connect(host="localhost", user="admin", password="odroid123", database="FYS")

if conn.is_connected():
    db_Info = conn.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
else:
    print("Connection failed to establish")


@app.route('/')
def index():
    return render_template("index.html")


def distance():
    # set Trigger to HIGH
    wpi.digitalWrite(triggerPin, wpi.HIGH)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
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

    return distance


def databaseInsert():
    with app.app_context():
        if __name__ == '__main__':
            try:
                while True:
                    dist = distance()
                    print("Measured Distance = %.1f cm" % dist)
                    time.sleep(1)
                    cursor = conn.cursor()

                    insert = "INSERT INTO Ultrasonic (data) VALUES (%s)"
                    cursor.execute(insert, [dist])
                    conn.commit()

                # Reset by pressing CTRL + C
            except KeyboardInterrupt:
                print("Measurement stopped by User")

@app.route('/api')
def fetchApi():
    return jsonify({'waardeselect': data })


@app.route('/sensoren')
def databaseRead():
    with app.app_context():
        cursorRead = conn.cursor()
        cursorRead.execute("select * from Ultrasonic ORDER BY id DESC LIMIT 20")
        data = cursorRead.fetchall()  # data from database.
    return render_template("sensoren.html", value=data)


sensorThread = threading.Thread(target=distance)
insertThread = threading.Thread(target=databaseInsert)
readThread = threading.Thread(target=databaseRead)


sensorThread.start()
insertThread.start()
readThread.start()

app.run(host="0.0.0.0", port=80, debug=True)


