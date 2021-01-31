from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://admin:1hospital@hospital-db-v2.cowul8deiwyt.ap-south-1.rds.amazonaws.com/hospital"
db = SQLAlchemy(app)


from models import User

print(*User.query.all(), sep="\n")


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
