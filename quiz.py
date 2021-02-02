from flask import Blueprint, render_template, redirect, session, url_for, flash
from flask_login import current_user

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

    # render the quiz
    return render_template("quiz.html", name=quiz_id)
