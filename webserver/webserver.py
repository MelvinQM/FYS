# Importeren van alle python packages
from flask import Flask, render_template, request, redirect, jsonify
import sys
import odroid_wiringpi as wpi
import time
import subprocess
# import threading
import ldr
import json

is_gestart = False

# Main flask code stuk
app = Flask(__name__, template_folder=".")

# Home Page
@app.route("/")
def home():
    head = "Welkom bij robothockey"
    greet = "Hello World"
    return render_template("index.html", head=head, greet=greet)


# Start de game loop
@app.route("/api")
def page1():
    wpi.wiringPiSetup()
    readldr = wpi.digitalRead(9)
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com',
                    'Yomamma': 69})

app.run(host="0.0.0.0", port=80, debug=True)
