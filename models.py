from app import db
from sqlalchemy.dialects.postgresql import JSON

class EmailData(db.Model):
    __tablename__ = 'email_data'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    from_email = db.Column(db.String)
    to_email = db.Column(db.String)
    email_message = db.Column(db.String)

    def __init__(self, id, title, from_email, to_email, email_message):
        self.id = id
        self.title = title
        self.from_email = from_email
        self.to_email = to_email
        self.email_message = email_message

    def __repr__(self):
        return '<id {}>'.format(self.id)