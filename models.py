import json
from collections import OrderedDict
from app import db
from sqlalchemy.dialects.postgresql import JSON

class EmailData(db.Model):
    __tablename__ = 'email_data'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    from_email = db.Column(db.String)
    to_email = db.Column(db.String)
    email_message = db.Column(db.String)
    email_sent = db.Column(db.String)

    def __init__(self, title, from_email, to_email, email_message, email_sent):
        self.title = title
        self.from_email = from_email
        self.to_email = to_email
        self.email_message = email_message
        self.email_sent = email_sent

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result