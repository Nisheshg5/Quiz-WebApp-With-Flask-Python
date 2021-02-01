from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class QuizIdForm(FlaskForm):
    quiz_id = StringField("quiz_id", validators=[DataRequired(), Length(min=5, max=10)])
    submit = SubmitField("Open Quiz")
