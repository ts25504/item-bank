from app import db


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
        }
        return json

    @staticmethod
    def generate_fake(count=1):
        import forgery_py

        for i in range(count):
            s = Subject(name=forgery_py.lorem_ipsum.word())

            db.session.add(s)
            db.session.commit()
