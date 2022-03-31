from flask import session
from flask_socketio import join_room, leave_room
from datetime import datetime



from Message import MessageModel
from SharedContext import *

import uuid

class JustAskSocketServer:

    def __init__(self):
        super().__init__()
        socketio.on_event("REQ_SEND_MESSAGE", self.REQUEST_SEND_MESSAGE)
        socketio.on_event("REQ_JOIN", self.REQUEST_JOIN)
        socketio.on_event("REQ_LEAVE", self.REQUEST_LEAVE)
        socketio.on_event("REQ_MESSAGE_VOTE_CHANGE", self.REQ_MESSAGE_VOTE_CHANGE)


    def REQUEST_SEND_MESSAGE(self,data):
        print("RECEIVED")
        data["time"] = datetime.now().strftime("%D %H:%M")   
        data["username"] = session["username"]                    
        data["message_id"] = str(uuid.uuid4())    
        data["session_id"] = session["active_session"]       

        socketio.emit('ACK_SEND_MESSAGE',data, to=session['active_session'])
        db.session.add(MessageModel(message_id = data["message_id"], message_flairs="flairs", date_sent = data["time"], num_upvotes=0,payload=data["message"], from_session_id=session["active_session"], from_user = session["username"]))
        db.session.commit()
    

    def REQ_MESSAGE_VOTE_CHANGE(self, data):

        # TODO MAKE THIS ENTIRE OPERATION ATOMIC
        message = MessageModel.query.filter_by(message_id = data["message_id"]).first()
        message.num_upvotes = int(data["vote_amount"])

        db.session.commit()
        socketio.emit("ACK_VOTE_CHANGE", {"message_id" : data["message_id"], "vote_amount" : data["vote_amount"]}, to=data["session_id"])


    def REQUEST_JOIN(self,data):
        join_room(session['active_session'])
        data["time"] = datetime.now().strftime("[%H:%M:%S]")
        data["username"] = session["username"]         
        socketio.emit('ACK_JOIN',data, room=session['active_session'], username=session["username"])

    def REQUEST_LEAVE(self,data):
        leave_room(session['active_session'])
        socketio.emit('ACK_LEAVE', data, room=session['active_session'])

