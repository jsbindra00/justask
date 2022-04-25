from enum import IntEnum
from ModelBase import ModelBase
from SharedContext import db



class MessagePacket(IntEnum):
    mcq_id = 0
    question = 1
    option_1 = 2
    option_2 = 3
    option_3 = 4
    option_4 = 5
    option_1_vote = 6
    option_2_vote = 7
    option_3_vote = 8
    option_4_vote = 9
    room = 10
    poll_history = 11
    from_user = 12



class MCQModel(db.Model):
    __bind_key__ = "mcq"

    mcq_id = db.Column(db.String(120), unique=False, nullable=False, primary_key=True)
    from_user = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    question = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    option_1 = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    option_2 = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    option_3 = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    option_4 = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)
    option_1_vote = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    option_2_vote = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    option_3_vote = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    option_4_vote = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    room = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)

    def __repr__(self):
        return 'MCQ {} {} {} {} {} {} {} {} {} {} {}'.format(self.mcq_id, self.from_user, self.question, self.option_1, self.option_2, self.option_3, self.option_4, self.option_1_vote, self.option_2_vote, self.option_3_vote, self.option_4_vote, self.room) 
    def __init__(self, **kwargs):
        super(MCQModel, self).__init__(**kwargs)

    def SaveDatabase(filePath):
        # pull all clients.
        ModelBase.ProcessDatabase(MCQModel.query.all(), filePath)
        print("SAVED MCQ DB TO {}".format(filePath))

    def PollToJSON(self):
     return {
        MessagePacket.mcq_id.name : self.mcq_id,
        MessagePacket.from_user.name : self.from_user,
        MessagePacket.question.name : self.question,
        MessagePacket.option_1.name : self.option_1,
        MessagePacket.option_2.name: self.option_2,
        MessagePacket.option_3.name : self.option_3,
        MessagePacket.room.name : self.room,
        MessagePacket.option_4.name : self.option_4,
        MessagePacket.option_1_vote.name : self.option_1_vote,
        MessagePacket.option_2_vote.name : self.option_2_vote,
        MessagePacket.option_3_vote.name : self.option_3_vote,
        MessagePacket.option_4_vote.name : self.option_4_vote,
    }
    










