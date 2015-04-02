from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class SingleChoice(db.Model):
    __tablename__ = 'single_choice'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text())
    difficult_level = db.Column(db.Enum('A', 'B', 'C', 'D', 'E'))
    add_date = db.Column(db.DateTime(), default=datetime.utcnow)
    faq = db.Column(db.Text())
    score = db.Column(db.Integer)

    answer = db.Column(db.Enum('A', 'B', 'C', 'D'))
    A = db.Column(db.String(64))
    B = db.Column(db.String(64))
    C = db.Column(db.String(64))
    D = db.Column(db.String(64))

class BlankFill(db.Model):
    __tablename__ = 'blank_fill'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text())
    difficult_level = db.Column(db.Enum('A', 'B', 'C', 'D', 'E'))
    add_date = db.Column(db.DateTime(), default=datetime.utcnow)
    faq = db.Column(db.Text())
    score = db.Column(db.Integer)

    answer = db.Column(db.String(64))

class Essay(db.Model):
    __tablename = 'essay'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text())
    difficult_level = db.Column(db.Enum('A', 'B', 'C', 'D', 'E'))
    add_date = db.Column(db.DateTime(), default=datetime.utcnow)
    faq = db.Column(db.Text())
    score = db.Column(db.Integer)
