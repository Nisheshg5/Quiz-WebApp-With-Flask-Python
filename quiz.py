from flask import Blueprint, render_template

quiz = Blueprint("quiz", __name__, static_folder="static", template_folder="templates")


@quiz.route("/<quiz_id>")
def quiz_page(quiz_id):
    return render_template("quiz.html", name=quiz_id)
