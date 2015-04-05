from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from markdown import markdown
import bleach
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
    question_html = db.Column(db.Text)
    difficult_level = db.Column(db.Enum('A', 'B', 'C', 'D', 'E'))
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    faq_html = db.Column(db.Text)
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    answer = db.Column(db.Enum('A', 'B', 'C', 'D'))
    A = db.Column(db.String(255))
    B = db.Column(db.String(255))
    C = db.Column(db.String(255))
    D = db.Column(db.String(255))

    @staticmethod
    def on_changed_question(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'br']
        attrs = {'*' : ['class'], 'a' : ['href', 'rel'], 'img' : ['src', 'alt'],}
        target.question_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

    @staticmethod
    def on_changed_faq(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'br']
        attrs = {'*' : ['class'], 'a' : ['href', 'rel'], 'img' : ['src', 'alt'],}
        target.faq_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

db.event.listen(SingleChoice.question, 'set', SingleChoice.on_changed_question)
db.event.listen(SingleChoice.faq, 'set', SingleChoice.on_changed_faq)

class BlankFill(db.Model):
    __tablename__ = 'blank_fill'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    question_html = db.Column(db.Text)
    difficult_level = db.Column(db.Enum('A', 'B', 'C', 'D', 'E'))
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    faq_html = db.Column(db.Text)
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    answer = db.Column(db.String(255))

    @staticmethod
    def on_changed_question(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'br']
        attrs = {'*' : ['class'], 'a' : ['href', 'rel'], 'img' : ['src', 'alt'],}
        target.question_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

    @staticmethod
    def on_changed_faq(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'br']
        attrs = {'*' : ['class'], 'a' : ['href', 'rel'], 'img' : ['src', 'alt'],}
        target.faq_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

db.event.listen(BlankFill.question, 'set', BlankFill.on_changed_question)
db.event.listen(BlankFill.faq, 'set', BlankFill.on_changed_faq)

class Essay(db.Model):
    __tablename = 'essay'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    question_html = db.Column(db.Text)
    difficult_level = db.Column(db.Enum('A', 'B', 'C', 'D', 'E'))
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    faq_html = db.Column(db.Text)
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    answer = db.Column(db.Text)
    answer_html = db.Column(db.Text)

    @staticmethod
    def on_changed_question(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'br']
        attrs = {'*' : ['class'], 'a' : ['href', 'rel'], 'img' : ['src', 'alt'],}
        target.question_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

    @staticmethod
    def on_changed_faq(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'br']
        attrs = {'*' : ['class'], 'a' : ['href', 'rel'], 'img' : ['src', 'alt'],}
        target.faq_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

    @staticmethod
    def on_changed_answer(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'br']
        attrs = {'*' : ['class'], 'a' : ['href', 'rel'], 'img' : ['src', 'alt'],}
        target.answer_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, attributes=attrs, strip=True))

db.event.listen(Essay.question, 'set', Essay.on_changed_question)
db.event.listen(Essay.faq, 'set', Essay.on_changed_faq)
db.event.listen(Essay.answer, 'set', Essay.on_changed_answer)
