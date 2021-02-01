from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from admin import admin
from forms import LoginForm, QuizIdForm, RegistrationForm
from login import login
from quiz import quiz
from user_profile import user_profile

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890abc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
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

# print(*User.query.all(), sep="\n", end="\n\n\n\n\n")
# print(*Quiz.query.all(), sep="\n", end="\n\n\n\n\n")
# print(*Question.query.all(), sep="\n", end="\n\n\n\n\n")
# print(*Question_choices.query.all(), sep="\n", end="\n\n\n\n\n")
# print(*User_question_answer.query.all(), sep="\n")

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(quiz, url_prefix="/quiz")
app.register_blueprint(user_profile, url_prefix="/user")


@app.context_processor
def inject_forms():
    loginForm = LoginForm()
    registrationForm = RegistrationForm()
    return dict(loginForm=loginForm, registrationForm=registrationForm)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        quizIdForm = QuizIdForm(request.form)
        if quizIdForm.submit.data and quizIdForm.validate_on_submit():
            if (
                Quiz.query.filter_by(quiz_id=quizIdForm.quiz_id.data).first()
                is not None
            ):
                return redirect(
                    url_for("quiz.quiz_page", quiz_id=quizIdForm.quiz_id.data)
                )
            else:
                flash(message=["Invalid Code"], category="error")
        else:
            flash(message=quizIdForm, category="validation")

    quizIdForm = QuizIdForm()
    return render_template("home.html", quizIdForm=quizIdForm)


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
