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


from app import db
from enum import IntEnum



class MessageModel(db.Model):
    __bind_key__ = "messages"

    message_id = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)
    message_flairs = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    date_sent = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    num_upvotes = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    payload = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    from_session_id = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    from_user = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)




    def __repr__(self):
        return 'MESSAGE {} {} {} {} {} {} {}'.format(self.message_id, self.message_flairs, self.date_sent, self.num_upvotes, self.payload, self.from_session_id, self.from_user) 
    def __init__(self, **kwargs):
        super(MessageModel, self).__init__(**kwargs)


    
    def SaveDatabase(filePath):
        # pull all clients.
        ModelBase.ProcessDatabase(MessageModel.query.all(), filePath)
        print("SAVED MESSAGES DB TO {}".format(filePath))










