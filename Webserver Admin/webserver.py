from flask import Flask, render_template
# import mysql.connector

# Main flask code stuk
app = Flask(__name__)

# conn = mysql.connector.connect("Hostname","dbusername","password","dbname" )
# cursor = conn.cursor()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sensoren')
def database():
# # cursor.execute("select * from table_name")
# # data = cursor.fetchall()  # data from database.
    return render_template("base.html")

app.run(host="0.0.0.0", port=80, debug=True)


