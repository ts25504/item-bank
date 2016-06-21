from app import db


class Points(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))
    subject = db.Column(db.Integer)
    subject_name = db.Column(db.String(127))
