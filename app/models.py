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
    subject = db.Column(db.Integer)
    knowledge_points_name = db.Column(db.String(127))
    subject_name = db.Column(db.String(127))

    answer = db.Column(db.Enum('A', 'B', 'C', 'D'))
    A = db.Column(db.String(255))
    B = db.Column(db.String(255))
    C = db.Column(db.String(255))
    D = db.Column(db.String(255))

    @staticmethod
    def generate_fake(count=200):
        from random import seed, random, randint, choice
        from models import Points, Subject
        import forgery_py

        seed()
        for i in range(count):
            sc = SingleChoice(question=forgery_py.lorem_ipsum.sentence(),
                    difficult_level=random(),
                    faq=forgery_py.lorem_ipsum.sentence(),
                    knowledge_points=randint(1, 10),
                    subject=1,
                    answer=choice(['A', 'B', 'C', 'D']),
                    A=forgery_py.lorem_ipsum.sentence(),
                    B=forgery_py.lorem_ipsum.sentence(),
                    C=forgery_py.lorem_ipsum.sentence(),
                    D=forgery_py.lorem_ipsum.sentence())

            p = Points.query.filter_by(id=sc.knowledge_points).first()
            sc.knowledge_points_name = p.name
            s = Subject.query.filter_by(id=sc.subject).first()
            sc.subject_name = s.name

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
    subject = db.Column(db.Integer)
    knowledge_points_name = db.Column(db.String(127))
    subject_name = db.Column(db.String(127))

    answer = db.Column(db.String(255))

    @staticmethod
    def generate_fake(count=200):
        from random import seed, random, randint
        from models import Points, Subject
        import forgery_py

        seed()
        for i in range(count):
            bf = BlankFill(question=forgery_py.lorem_ipsum.sentence(),
                    difficult_level=random(),
                    faq=forgery_py.lorem_ipsum.sentence(),
                    knowledge_points=randint(1, 10),
                    subject=1,
                    answer=forgery_py.lorem_ipsum.sentence())

            p = Points.query.filter_by(id=bf.knowledge_points).first()
            bf.knowledge_points_name = p.name
            s = Subject.query.filter_by(id=bf.subject).first()
            bf.subject_name = s.name

            db.session.add(bf)
            db.session.commit()

class Essay(db.Model):
    __tablename__ = 'essay'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    difficult_level = db.Column(db.Float)
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    knowledge_points = db.Column(db.Integer)
    subject = db.Column(db.Integer)
    knowledge_points_name = db.Column(db.String(127))
    subject_name = db.Column(db.String(127))

    answer = db.Column(db.Text)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, random, randint
        from models import Points, Subject
        import forgery_py

        seed()
        for i in range(count):
            es = Essay(question=forgery_py.lorem_ipsum.sentence(),
                    difficult_level=random(),
                    faq=forgery_py.lorem_ipsum.sentence(),
                    knowledge_points=randint(1, 10),
                    subject=1,
                    answer=forgery_py.lorem_ipsum.sentence())

            p = Points.query.filter_by(id=es.knowledge_points).first()
            es.knowledge_points_name = p.name
            s = Subject.query.filter_by(id=es.subject).first()
            es.subject_name = s.name

            db.session.add(es)
            db.session.commit()

class Points(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))
    subject = db.Column(db.Integer)
    subject_name = db.Column(db.String(127))

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))

class TestPaper(db.Model):
    __tablename__ = 'test_paper'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    subject = db.Column(db.Integer)
    subject_name = db.Column(db.String(127))
    single_choice = db.Column(db.String(255))
    blank_fill = db.Column(db.String(255))
    essay = db.Column(db.String(255))
    add_date = db.Column(db.Date, default=date.today)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
