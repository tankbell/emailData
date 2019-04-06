from app import db
from sqlalchemy.dialects.postgresql import JSON

class EmailData(db.Model):
    __tablename__ = 'emails'

    title = db.Column(db.String, primary_key=True)
    from_email = db.Column(db.String)
    to_email = db.Column(db.String)
    email_message = db.Column(db.String)

    def __init__(self, title, from_email, to_email, email_message):
        self.title = title
        self.from_email = from_email
        self.to_email = to_email
        self.email_message = email_message

    def __repr__(self):
        return '<title {}>'.format(self.title)