from flask import Flask
import odroid_wiringpi as wpi

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"
@app.route("/page1")
def page1():
    return "Page 1"

if 0 == 0:
    app.run(host="0.0.0.0", port=80, debug=True)
