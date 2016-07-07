from datetime import date, datetime
from app import db
from app.model.point_model import Points
from app.model.subject_model import Subject


class BlankFill(db.Model):
    __tablename__ = 'blank_fill'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    difficult_level = db.Column(db.Float)
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    points_id = db.Column(db.Integer, db.ForeignKey('points.id'))
    points = db.relationship('Points', backref='blank_fill')
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', backref='blank_fill')

    answer = db.Column(db.String(255))

    def to_json(self):
        json = {
            'question': self.question,
            'difficult_level': self.difficult_level,
            'faq': self.faq,
            'timestamp': self.timestamp,
            'points': self.points.name,
            'subject': self.subject.name,
            'answer': self.answer,
        }
        return json

    @staticmethod
    def generate_fake(count=200):
        from random import seed, random, choice
        import forgery_py

        subject_ids = [s.id for s in Subject.query.all()]
        point_ids = [p.id for p in Points.query.all()]

        seed()
        for i in range(count):
            bf = BlankFill(question=forgery_py.lorem_ipsum.sentence(),
                           difficult_level=random(),
                           faq=forgery_py.lorem_ipsum.sentence(),
                           points_id=choice(point_ids),
                           subject_id=choice(subject_ids),
                           answer=forgery_py.lorem_ipsum.sentence())

            db.session.add(bf)
            db.session.commit()
