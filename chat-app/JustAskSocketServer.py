from email.message import Message
from tkinter import Pack
from flask import session
from flask_socketio import join_room, leave_room
from datetime import datetime
from Client import ClientModel, ClientAttribute


from Message import MessageModel, PacketAttributes
from MCQ import MCQModel, MessagePacket
from SharedContext import *

import uuid
import time

class JustAskSocketServer:

    def __init__(self):
        super().__init__()
        socketio.on_event("REQ_SEND_MESSAGE", self.REQUEST_SEND_MESSAGE)
        socketio.on_event("REQ_JOIN", self.REQUEST_JOIN)
        socketio.on_event("REQ_LEAVE", self.REQUEST_LEAVE)
        socketio.on_event("REQ_MESSAGE_VOTE_CHANGE", self.REQ_MESSAGE_VOTE_CHANGE)
        socketio.on_event("REQ_MESSAGE_CACHE_UPDATE", self.REQUEST_MESSAGE_CACHE_UPDATE)

        
        socketio.on_event("REQ_SEND_POLL", self.REQUEST_SEND_POLL)
        socketio.on_event("REQ_SEND_POLL_VOTE", self.REQUEST_SEND_POLL_VOTE)
        socketio.on_event('REQ_POLL_CACHE', self.REQUEST_POLL_CACHE)

    def isAnonymous(self):
        if session["ANONYMOUS"] == True:
            return "Anon"
        return  session["USERNAME"]
    
    def REQUEST_POLL_CACHE(self, data):
        poll_history = {
            "username" : self.isAnonymous(),
            MessagePacket.poll_history.name : [poll.PollToJSON() for poll in MCQModel.query.filter_by(**{MessagePacket.room.name:data[MessagePacket.room.name]}).all()]
            }
        socketio.emit("ACK_POLL_CACHE_UPDATE", poll_history)

    def REQUEST_SEND_POLL(self, data):
        data["mcq_id"] = str(uuid.uuid4())
        data["session_id"] = session["ACTIVE_SESSION"]
        data["vote1"] = 0
        data["vote2"] = 0
        data["vote3"] = 0
        data["vote4"] = 0
        data["vote5"] = 0
        data["vote6"] = 0
        data["vote_count"] = 0

        active_clients = [client.USERNAME for client in ClientModel.query.filter_by(ACTIVE_SESSION=data["session_id"]).all()]
        for active_user in active_clients:
            db.session.add(MCQModel(mcq_id= data["mcq_id"],from_user=active_user,room=data["session_id"], question=data["question"], option_1=data["option1"], option_2=data["option2"], option_3=data["option3"],option_4=data["option4"], option_1_vote=data["vote1"], option_2_vote=data["vote2"], option_3_vote=data["vote3"], option_4_vote=data["vote4"] ))
        db.session.commit()
        socketio.emit('ACK_SEND_POLL', data)
    
    def REQUEST_MESSAGE_CACHE_UPDATE(self, data):
        message_history = {PacketAttributes.MESSAGE_HISTORY.name : [message.MessageToJSON() for message in MessageModel.query.filter_by(**{PacketAttributes.from_session_id.name:data[PacketAttributes.from_session_id.name]}).all()]}
        socketio.emit("ACK_MESSAGE_CACHE_UPDATE", message_history)
        # convert messages to JSON.

    def REQUEST_SEND_MESSAGE(self,data):
        data["username"] = self.isAnonymous()
        data["time"] = datetime.now().strftime("%D %H:%M")  
        data["message_id"] = str(uuid.uuid4())    
        data["session_id"] = session["ACTIVE_SESSION"]
        data["vote_count"] = 0
        data["time_since_epoch"] = time.time()
        message_flairs =";".join(data["FLAIRS"]) 
        db.session.add(MessageModel(message_id = data["message_id"], FLAIRS=message_flairs, date_sent = data["time"], num_upvotes=0,payload=data["message"], from_session_id=session["ACTIVE_SESSION"], from_user = session["USERNAME"],time_since_epoch = data["time_since_epoch"],FROM_PARENT_ID = data["FROM_PARENT_ID"], IS_ANON = session["ANONYMOUS"]))
        db.session.commit()
        socketio.emit('ACK_SEND_MESSAGE',data, to=session['ACTIVE_SESSION'])

    

    def REQ_MESSAGE_VOTE_CHANGE(self, data):
    
        # TODO MAKE THIS ENTIRE OPERATION ATOMIC
        message = MessageModel.query.filter_by(message_id = data["message_id"]).first()
        message.num_upvotes = int(data["vote_amount"])

        db.session.commit()
        socketio.emit("ACK_VOTE_CHANGE", {"message_id" : data["message_id"], "vote_amount" : data["vote_amount"]}, to=data["session_id"])

    def REQUEST_JOIN(self,data):
        join_room(session['ACTIVE_SESSION'])
        data["time"] = datetime.now().strftime("[%H:%M:%S]")
        data["username"] = self.isAnonymous()
        data["ACTIVE_SESSION"] = session["ACTIVE_SESSION"]
        socketio.emit('ACK_JOIN',data, room=data["ACTIVE_SESSION"], username=data["username"])

    def REQUEST_LEAVE(self,data):
        leave_room(session['ACTIVE_SESSION'])
        socketio.emit('ACK_LEAVE', data, room=session['ACTIVE_SESSION'])

    def REQUEST_SEND_POLL_VOTE(self, data):
        
        poll = MCQModel.query.filter_by(mcq_id = data["mcq_id"]).first()
        attr = "option_" + str(data["index"]) + "_vote"
        setattr(poll, attr, int(getattr(poll, attr)+1))

        db.session.commit()

        new_data = {"index" : data["index"], "mcq_id" : data["mcq_id"]}
        for i in range(4):
            new_data["option_" + str(i+1)+ "_vote"] = getattr(poll, "option_" + str(i+1) + "_vote")
        socketio.emit('ACK_POLL_VOTE', new_data)


        