from app import db


class Points(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', backref='points')

    @staticmethod
    def generate_fake(count=10):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            p = Points(name=forgery_py.lorem_ipsum.word(),
                       subject_id=1)

            db.session.add(p)
            db.session.commit()
