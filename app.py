from datetime import datetime

from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)


mysql = MySQL()
app.config[
    "MYSQL_DATABASE_HOST"
] = "hospital-db-v2.cowul8deiwyt.ap-south-1.rds.amazonaws.com"
app.config["MYSQL_DATABASE_USER"] = "admin"
app.config["MYSQL_DATABASE_PASSWORD"] = "1hospital"
app.config["MYSQL_DATABASE_DB"] = "hospital"
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

cursor.execute("SELECT * from doctor")
print(*cursor.fetchall(), sep="\n")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name=None):
    return render_template("hello_there.html", name=name, date=datetime.now())


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
