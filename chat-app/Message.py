from enum import IntEnum


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


from app import clientsDB
from enum import IntEnum



class MessageModel(clientsDB.Model):


    messageid = clientsDB.Column(clientsDB.String(120), unique=True, nullable=False, primary_key=True)

    messageid = 
    email = clientsDB.Column(clientsDB.String(120), unique=True, nullable=False, primary_key=True)
    username = clientsDB.Column(clientsDB.String(80), unique=True, nullable=False)
    firstname = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    lastname = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    password = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    active_session = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    def __init__(self, **kwargs):
        super(MessageModel, self).__init__(**kwargs)








