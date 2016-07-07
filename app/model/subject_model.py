from app import db


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))

    @staticmethod
    def generate_fake(count=1):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            s = Subject(name=forgery_py.lorem_ipsum.word())

            db.session.add(s)
            db.session.commit()
