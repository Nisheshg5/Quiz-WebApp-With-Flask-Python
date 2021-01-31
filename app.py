from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
url = "mysql://{0}:{1}@{2}:{3}/{4}".format(
    "adminsql@quiz-mysql-db",
    "Quiz@123",
    "quiz-mysql-db.mysql.database.azure.com",
    3306,
    "quiz",
)
app.config["SQLALCHEMY_DATABASE_URI"] = url
db = SQLAlchemy(app)


from models import Question, Question_choices, Quiz, User, User_question_answer

print(*User.query.all(), sep="\n", end="\n\n\n\n\n")
print(*Quiz.query.all(), sep="\n", end="\n\n\n\n\n")
print(*Question.query.all(), sep="\n", end="\n\n\n\n\n")
print(*Question_choices.query.all(), sep="\n", end="\n\n\n\n\n")
print(*User_question_answer.query.all(), sep="\n")


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
