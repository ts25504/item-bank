from datetime import date, datetime
from app import db


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
