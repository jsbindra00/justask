from enum import IntEnum
from ModelBase import ModelBase


from SharedContext import db
from enum import IntEnum





class PacketAttributes(IntEnum):
    MESSAGE_ID = 0
    MESSAGE_FLAIRS = 1
    DATE_SENT = 2
    NUM_UPVOTES = 3
    PAYLOAD = 4
    from_session_id = 5
    FROM_USER = 6
    MESSAGE_HISTORY = 7


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

    def MessageToJSON(self):
        return {
            PacketAttributes.MESSAGE_ID.name : self.message_id,
            PacketAttributes.MESSAGE_FLAIRS.name : self.message_flairs,
            PacketAttributes.DATE_SENT.name : self.date_sent,
            PacketAttributes.NUM_UPVOTES.name: self.num_upvotes,
            PacketAttributes.PAYLOAD.name : self.payload,
            PacketAttributes.from_session_id.name : self.from_session_id,
            PacketAttributes.FROM_USER.name : self.from_user
        }










