from datetime import datetime, timedelta

from flask import Flask, flash, redirect, render_template, request, session, url_for
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

app.permanent_session_lifetime = timedelta(minutes=30)

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
@app.route("/home", methods=["GET", "POST"])
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
            errors = [
                [quizIdForm[a].label.text, b] for a, b in quizIdForm.errors.items()
            ]
            flash(message=errors, category="validation")

    quizIdForm = QuizIdForm()
    session["redirectURL"] = {"endpoint": "home"}
    return render_template("home.html", quizIdForm=quizIdForm)


@app.route("/about/")
def about():
    session["redirectURL"] = {"endpoint": "about"}
    return render_template("about.html")


@app.route("/contact/")
def contact():
    session["redirectURL"] = {"endpoint": "contact"}
    return render_template("contact.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name=None):
    session["redirectURL"] = {"endpoint": "hello_there", "name": name}
    return render_template("hello_there.html", name=name, date=datetime.now())


@app.route("/api/data")
def get_data():
    session["redirectURL"] = {"endpoint": "get_data"}
    return app.send_static_file("data.json")


@app.route("/login", methods=["GET", "POST"])
def login():
    loginForm = LoginForm(request.form)
    if loginForm.loginSubmit.data and loginForm.validate_on_submit():
        user = (
            User.query.filter_by(email=loginForm.email.data)
            .filter_by(password=loginForm.password.data)
            .first()
        )
        if user is not None:
            session.permanent = True
            session["loggedIn"] = True
            session["user"] = user
            session["user_id"] = user.user_id
            flash(
                message=[
                    f"Logged in successfully",
                    f"Welcome {user.username.capitalize()}",
                ],
                category="success",
            )
            return redirect(url_for(**session["redirectURL"]))
        else:
            flash(message=["Invalid username or password"], category="error")
            return redirect(url_for(**session["redirectURL"]))
    else:
        errors = [[loginForm[a].label.text, b] for a, b in loginForm.errors.items()]
        flash(message=errors, category="validation")
        return redirect(url_for(**session["redirectURL"]))


@app.route("/register", methods=["GET", "POST"])
def register():
    registrationForm = RegistrationForm(request.form)
    if (
        registrationForm.registrationSubmit.data
        and registrationForm.validate_on_submit()
    ):
        if User.query.filter_by(email=registrationForm.email.data).first() is None:
            flash(message=["User created successfully"], category="success")
            return redirect(**session["redirectURL"])
        else:
            flash(
                message=["User already exists. Please Log in instead"],
                category="warning",
            )
            return redirect(**session["redirectURL"])
    else:
        errors = [
            [registrationForm[a].label.text, b]
            for a, b in registrationForm.errors.items()
        ]
        flash(message=errors, category="validation")
        return redirect(**session["redirectURL"])


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "error.html",
        code=404,
        title="404 Not Found",
        content=" The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
        content_secondary="",
    )


@app.errorhandler(500)
def page_not_found(e):
    return render_template(
        "error.html",
        code=500,
        title="Internal Server Error",
        content="The server encountered an internal error and was unable to complete your request.",
        content_secondary="Please try again later.",
    )
