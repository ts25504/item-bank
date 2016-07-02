from datetime import date, datetime
from app import db


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
    def generate_fake(count=100):
        from random import seed, random, randint
        import forgery_py

        seed()
        for i in range(count):
            es = Essay(question=forgery_py.lorem_ipsum.paragraph(),
                       difficult_level=random(),
                       faq=forgery_py.lorem_ipsum.sentence(),
                       points_id=randint(1, 10),
                       subject_id=1,
                       answer=forgery_py.lorem_ipsum.paragraph())

            db.session.add(es)
            db.session.commit()
