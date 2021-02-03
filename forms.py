from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class QuizIdForm(FlaskForm):
    quiz_id = StringField(
        "Quiz Code",
        render_kw={"placeholder": "Enter Code"},
        validators=[DataRequired(), Length(min=1, max=3)],
    )
    submitBtn = SubmitField("Open Quiz")


class QuizPwdForm(FlaskForm):
    quiz_pwd = StringField(
        "Quiz Password",
        render_kw={"placeholder": "Enter password"},
        validators=[DataRequired(), Length(min=1, max=4)],
    )
    submitPwd = SubmitField("Enter Quiz")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        render_kw={"placeholder": "Email"},
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Enter Password"},
        validators=[DataRequired(), Length(min=8, max=16)],
    )
    remember = BooleanField("Remember Me")
    loginSubmit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField(
        "Email",
        render_kw={"placeholder": "Email"},
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Enter Password"},
        validators=[DataRequired(), Length(min=8, max=16)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        render_kw={"placeholder": "Confirm Password"},
        validators=[DataRequired(), EqualTo("password")],
    )
    registrationSubmit = SubmitField("Sign Up")
