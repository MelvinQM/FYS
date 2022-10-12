# Importere van alle python packages
from flask import Flask, render_template, request
import sys
import odroid_wiringpi as wpi
import time

# Appenden van andere scripts
sys.path.append("/root/fasten-your-seatbelts/ldr_code")
import ldr
import ldr_test

app = Flask(__name__, template_folder=".")


@app.route("/")
def home():
    head = "Welkom bij robothockey"
    greet = "Hello World"
    return render_template("index.html", head=head, greet=greet)


@app.route("/maingameloop")
def page1():
    ldr.ldr_func()
    pagina1 = "Main Game Loop"
    return render_template("page2.html", page2=pagina1)


if 0 == 0:
    app.run(host="0.0.0.0", port=80, debug=True)
