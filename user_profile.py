from flask import Blueprint, render_template

user_profile = Blueprint("user_profile", __name__, static_folder="static", template_folder="templates")


@user_profile.route("/")
def profile_page():
    return render_template("profile.html")
