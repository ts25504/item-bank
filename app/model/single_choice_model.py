from datetime import date, datetime
from app import db
from app.model.point_model import Points
from app.model.subject_model import Subject


class SingleChoice(db.Model):
    __tablename__ = 'single_choice'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    difficult_level = db.Column(db.Float)
    add_date = db.Column(db.Date, default=date.today)
    faq = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    points_id = db.Column(db.Integer, db.ForeignKey('points.id'))
    points = db.relationship('Points', backref='single_choice')
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', backref='single_choice')

    answer = db.Column(db.Enum('A', 'B', 'C', 'D'))
    A = db.Column(db.Text)
    B = db.Column(db.Text)
    C = db.Column(db.Text)
    D = db.Column(db.Text)

    def to_json(self):
        json = {
            'question': self.question,
            'difficult_level': self.difficult_level,
            'faq': self.faq,
            'timestamp': self.timestamp,
            'points': self.points.name,
            'subject': self.subject.name,
            'answer': self.answer,
            'A': self.A,
            'B': self.B,
            'C': self.C,
            'D': self.D,
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
            sc = SingleChoice(question=forgery_py.lorem_ipsum.sentence(),
                              difficult_level=random(),
                              faq=forgery_py.lorem_ipsum.sentence(),
                              points_id=choice(point_ids),
                              subject_id=choice(subject_ids),
                              answer=choice(['A', 'B', 'C', 'D']),
                              A=forgery_py.lorem_ipsum.sentence(),
                              B=forgery_py.lorem_ipsum.sentence(),
                              C=forgery_py.lorem_ipsum.sentence(),
                              D=forgery_py.lorem_ipsum.sentence())

            db.session.add(sc)
            db.session.commit()
