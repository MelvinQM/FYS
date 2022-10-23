# Importeren van alle python packages
from flask import Flask, render_template, request, redirect
import sys
import odroid_wiringpi as wpi
import time
import subprocess
# import threading
import ldr

is_gestart = False

# Main flask code stuk
app = Flask(__name__, template_folder=".")


def spel():
    if is_gestart == true:
        pass


# Home Page
@app.route("/")
def home():
    head = "Welkom bij robothockey"
    greet = "Hello World"
    return render_template("index.html", head=head, greet=greet)


# Start de game loop
@app.route("/start")
def page1():
    wpi.wiringPiSetup()
    readldr = wpi.digitalRead(9)
    return render_template("maingameloop.html", readldr=readldr)


app.run(host="0.0.0.0", port=80, debug=True)
