from datetime import date, datetime
from app import db
from app.model.point_model import Points
from app.model.subject_model import Subject


class Essay(db.Model):
    __tablename__ = 'essay'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    difficult_level = db.Column(db.Float)
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    points_id = db.Column(db.Integer, db.ForeignKey('points.id'))
    points = db.relationship('Points', backref='essay')
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', backref='essay')

    answer = db.Column(db.Text)

    def to_json(self):
        json = {
            'id': self.id,
            'question': self.question,
            'difficult_level': self.difficult_level,
            'faq': self.faq,
            'timestamp': self.timestamp,
            'points': self.points_id,
            'subject': self.subject_id,
            'answer': self.answer,
        }
        return json

    @staticmethod
    def generate_fake(count=100):
        from random import seed, random, choice
        import forgery_py

        subject_ids = [s.id for s in Subject.query.all()]
        point_ids = [p.id for p in Points.query.all()]

        seed()
        for i in range(count):
            es = Essay(question=forgery_py.lorem_ipsum.paragraph(),
                       difficult_level=random(),
                       faq=forgery_py.lorem_ipsum.sentence(),
                       points_id=choice(point_ids),
                       subject_id=choice(subject_ids),
                       answer=forgery_py.lorem_ipsum.paragraph())

            db.session.add(es)
            db.session.commit()
