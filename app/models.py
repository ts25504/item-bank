from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
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
    question = db.Column(db.Text)
    difficult_level = db.Column(db.Float)
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    knowledge_points = db.Column(db.Integer)

    answer = db.Column(db.Enum('A', 'B', 'C', 'D'))
    A = db.Column(db.String(255))
    B = db.Column(db.String(255))
    C = db.Column(db.String(255))
    D = db.Column(db.String(255))

    @staticmethod
    def generate_fake(count=400):
        from random import seed, random, randint, choice
        import forgery_py

        seed()
        for i in range(count):
            sc = SingleChoice(question=forgery_py.lorem_ipsum.sentence(),
                    difficult_level=random(),
                    faq=forgery_py.lorem_ipsum.sentence(),
                    knowledge_points=randint(1, 10),
                    answer=choice(['A', 'B', 'C', 'D']),
                    A=forgery_py.lorem_ipsum.sentence(),
                    B=forgery_py.lorem_ipsum.sentence(),
                    C=forgery_py.lorem_ipsum.sentence(),
                    D=forgery_py.lorem_ipsum.sentence())

            db.session.add(sc)
            db.session.commit()

class BlankFill(db.Model):
    __tablename__ = 'blank_fill'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    difficult_level = db.Column(db.Float)
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    knowledge_points = db.Column(db.Integer)

    answer = db.Column(db.String(255))

    @staticmethod
    def generate_fake(count=300):
        from random import seed, random, randint
        import forgery_py

        seed()
        for i in range(count):
            bf = BlankFill(question=forgery_py.lorem_ipsum.sentence(),
                    difficult_level=random(),
                    faq=forgery_py.lorem_ipsum.sentence(),
                    knowledge_points=randint(1, 10),
                    answer=forgery_py.lorem_ipsum.sentence())
            db.session.add(bf)
            db.session.commit()

class Essay(db.Model):
    __tablename = 'essay'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    difficult_level = db.Column(db.Float)
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    knowledge_points = db.Column(db.Integer)

    answer = db.Column(db.Text)

    @staticmethod
    def generate_fake(count=300):
        from random import seed, random, randint
        import forgery_py

        seed()
        for i in range(count):
            es = Essay(question=forgery_py.lorem_ipsum.sentence(),
                    difficult_level=random(),
                    faq=forgery_py.lorem_ipsum.sentence(),
                    knowledge_points=randint(1, 10),
                    answer=forgery_py.lorem_ipsum.sentence())
            db.session.add(es)
            db.session.commit()
