from email.message import Message
from tkinter import Pack
from flask import session
from flask_socketio import join_room, leave_room
from datetime import datetime



from Message import MessageModel, PacketAttributes
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



    def REQUEST_MESSAGE_CACHE_UPDATE(self, data):
        message_history = {PacketAttributes.MESSAGE_HISTORY.name : [message.MessageToJSON() for message in MessageModel.query.filter_by(**{PacketAttributes.from_session_id.name:data[PacketAttributes.from_session_id.name]}).all()]}
        socketio.emit("ACK_MESSAGE_CACHE_UPDATE", message_history)
        # convert messages to JSON.

    def REQUEST_SEND_MESSAGE(self,data):
        data["time"] = datetime.now().strftime("%D %H:%M")   
        data["username"] = session["USERNAME"]                    
        data["message_id"] = str(uuid.uuid4())    
        data["session_id"] = session["ACTIVE_SESSION"]
        data["vote_count"] = 0
        data["time_since_epoch"] = time.time()
        
        db.session.add(MessageModel(message_id = data["message_id"], message_flairs="flairs", date_sent = data["time"], num_upvotes=0,payload=data["message"], from_session_id=session["ACTIVE_SESSION"], from_user = session["USERNAME"],time_since_epoch = data["time_since_epoch"],FROM_PARENT_ID = data["FROM_PARENT_ID"]))
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
        data["username"] = session["USERNAME"]         
        data["ACTIVE_SESSION"] = session["ACTIVE_SESSION"]
        socketio.emit('ACK_JOIN',data, room=session['ACTIVE_SESSION'], username=session["USERNAME"])

    def REQUEST_LEAVE(self,data):
        leave_room(session['ACTIVE_SESSION'])
        socketio.emit('ACK_LEAVE', data, room=session['ACTIVE_SESSION'])

