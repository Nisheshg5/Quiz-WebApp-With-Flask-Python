from datetime import datetime, time

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user

from forms import QuizIdForm, QuizPwdForm
from models import Quiz, User

quiz = Blueprint("quiz", __name__, static_folder="static", template_folder="templates")


@quiz.route("/", methods=["GET", "POST"])
def quiz_page():
    if request.method == "POST":
        quizIdForm = QuizIdForm(request.form)
        if quizIdForm.submitBtn.data and quizIdForm.validate_on_submit():
            if (
                Quiz.query.filter_by(quiz_id=quizIdForm.quiz_id.data).first()
                is not None
            ):
                return redirect(
                    url_for("quiz.quiz_page_id", quiz_id=quizIdForm.quiz_id.data)
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
    return redirect(url_for(**session["redirectURL"]))



@quiz.route("/<quiz_id>/instructions", methods=["GET", "POST"])
def quiz_instructions(quiz_id):

    if request.method == "POST":
        # user should be logged in
        if not current_user.is_authenticated:
            return redirect(url_for(**session["redirectURL"]))

        #validate form data
        quizPwdForm = QuizPwdForm(request.form)
        if quizPwdForm.submitPwd.data and quizPwdForm.validate_on_submit():
            quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
            if (quiz is not None):
                if(quiz.quiz_pwd == quizPwdForm.quiz_pwd.data):             #this line will throw error because the model doesn't contains that column
                    print("Password Matched ")
                    return("Welcome to instructions")
                else:
                    print("Passwod doesn't match")
                    flash(message=["Incorrect Password"], category="error")
                    return redirect(url_for(**session["redirectURL"]))
            else:
                print("Quiz not found with this id")
                flash(message=["Invalid Code"], category="error")
        else:
            print("Invalid Form input")
            errors = [
                [quizPwdForm[a].label.text, b] for a, b in quizPwdForm.errors.items()
            ]
            flash(message=errors, category="validation")

    return redirect(url_for(**session["redirectURL"]))

@quiz.route("/<quiz_id>")
def quiz_page_id(quiz_id):

    # user should be logged in
    if not current_user.is_authenticated:
        return redirect(url_for(**session["redirectURL"]))

    # should be a valid quiz_id
    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
    if not quiz:
        flash(message=["Invalid test code"], category="error")
        return redirect(url_for(**session["redirectURL"]))

    # check for quiz expiration
    # if the  quiz is expired we don't need to fetch the questions
    # expired

    # if(quiz.end_date < datetime.utcnow()):
    return render_template("quiz.html", quiz=quiz, datetime=datetime)