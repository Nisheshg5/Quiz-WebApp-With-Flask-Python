from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class QuizIdForm(FlaskForm):
    quiz_id = StringField(
        "Quiz Code", validators=[DataRequired(), Length(min=1, max=3)]
    )
    submit = SubmitField("Open Quiz")
