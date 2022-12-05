from flask import Flask, render_template
import mysql.connector

# Main flask code stuk
app = Flask(__name__)

conn = mysql.connector.connect(host="localhost", user="nick", password="odroid123", database="test")

if conn.is_connected():
    db_Info = conn.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
else:
    print("Connection failed to establish")

cursor = conn.cursor()



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sensoren')
def database():
    cursor.execute("select * from sensoren")
    data = cursor.fetchall()  # data from database.
    return render_template("sensoren.html", value=data)


app.run(host="0.0.0.0", port=80, debug=True)


