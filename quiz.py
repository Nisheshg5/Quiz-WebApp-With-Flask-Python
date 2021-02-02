from flask import Blueprint, render_template, redirect, session, url_for, flash
from flask_login import current_user
from datetime import datetime

from models import Quiz, User

quiz = Blueprint("quiz", __name__, static_folder="static", template_folder="templates")


@quiz.route("/")
def quiz_page():
    return redirect(url_for(**session["redirectURL"]))

@quiz.route("/<quiz_id>")
def quiz_page_id(quiz_id):

    # user should be logged in
    if not current_user.is_authenticated:
        return redirect(url_for(**session["redirectURL"]))


    # should be a valid quiz_id
    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
    if(not quiz):
        flash(message=["Invalid test code"], category="error")
        return redirect(url_for(**session["redirectURL"]))

    # check for quiz expiration
    # if the  quiz is expired we don't need to fetch the questions
    # expired
    
    if(quiz.end_date < datetime.utcnow()):        
        return render_template("quiz.html", id=quiz_id, title=quiz.title, start=quiz.start_date, end=quiz.end_date)
    else:
        return render_template("quiz.html",  id=quiz_id, title=quiz.title, start=quiz.start_date, end=quiz.end_date, questions=quiz.questions)

    
