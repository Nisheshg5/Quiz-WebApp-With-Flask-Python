from datetime import datetime, timedelta
from uuid import uuid4

from flask_login import UserMixin

from app import bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def default_start_datetime():
    return datetime.utcnow() + timedelta(hours=3)


def default_end_datetime():
    return datetime.utcnow() + timedelta(hours=6)


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_question_answers = db.relationship(
        "User_question_answer", backref="user", lazy=True
    )

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"user_id: {self.user_id}, username: {self.username}, email: {self.email}, password: {self.password}"


class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_code = db.Column(db.String(120), unique=True, default=lambda: uuid4().hex)
    title = db.Column(db.String(120), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=default_start_datetime)
    end_date = db.Column(db.DateTime, nullable=False, default=default_end_datetime)
    duration = db.Column(db.Integer, nullable=False, default=90)
    questions = db.relationship("Question", backref="quiz", lazy=True)

    def __repr__(self):
        return f"quiz_id: {self.quiz_id}, title: {self.title}"


class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id"), nullable=False)
    choices = db.relationship("Question_choices", backref="question", lazy=True)

    def __repr__(self):
        return f"question_id: {self.question_id}, question: {self.question}, quiz_id: {self.quiz_id}"


class Question_choices(db.Model):
    choices_id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.Text, nullable=False)
    is_right_choice = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.question_id"), nullable=False
    )

    def __repr__(self):
        return f"choices_id: {self.choices_id}, choice: {self.choice}, is_right_choice: {self.is_right_choice}, question_id: {self.question_id}"


class User_question_answer(db.Model):
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.user_id"), primary_key=True, nullable=False
    )
    quiz_id = db.Column(
        db.Integer, db.ForeignKey("quiz.quiz_id"), primary_key=True, nullable=False
    )
    question_id = db.Column(
        db.Integer,
        db.ForeignKey("question.question_id"),
        primary_key=True,
        nullable=False,
    )
    choice_id = db.Column(
        db.Integer, db.ForeignKey("question_choices.choices_id"), nullable=False
    )
    subitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_right = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"user_id: {self.user_id}, quiz_id: {self.quiz_id}, question_id: {self.question_id}, choice_id: {self.choice_id}, is_right: {self.is_right}"


def reset_db():
    db.create_all()
    db.session.add(
        Quiz(
            title="Vestibulum ac est lacinia nisi venenatis tristique.",
            instructions=""""line 1
                        line 2
                        line 3""",
            password=bcrypt.generate_password_hash("p").decode("utf8"),
        )
    )

    db.session.commit()


# reset_db()
