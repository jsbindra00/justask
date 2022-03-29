from enum import IntEnum
from ModelBase import ModelBase


class MessageAttribute(IntEnum):
    Flairs = 0 # list of flairs
    Upvotes = 1 # integer
    Date = 2
    MessageID = 3


class MessageFlairType(IntEnum):
    Message = 1
    Question = 2
    Request = 3


class Message:

    def __init__(self, flairs, upvotes, date, id):
        self.flairs = flairs
        self.upvotes = upvotes
        self.date = date
        self.messageID = id


from app import db
from enum import IntEnum



class MessageModel(db.Model):
    __bind_key__ = "messages"

    # messageid = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    active_session = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    def __init__(self, **kwargs):
        super(MessageModel, self).__init__(**kwargs)


    
    def SaveDatabase(filePath):
        # pull all clients.
        ModelBase.ProcessDatabase(MessageModel.query.all(), filePath)
        print("SAVED MESSAGES DB TO {}".format(filePath))








