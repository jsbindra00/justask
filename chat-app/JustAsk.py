from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room
import sqlite3
from datetime import datetime
from flask_classful import FlaskView, route

from Client import ClientModel
from Utility import Utility

from Message import Message
from app import *


class JustAsk(FlaskView):
    default_methods = ['GET', 'POST']
    route_base = "/"

    def __init__(self):
        db.create_all()
    def Start(self):
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_TYPE"] = "filesystem"
        Session(app)

        socketio.on_event("send_message", self.handle_send_message_event)
        socketio.on_event("join_room", self.handle_join_room_event)
        socketio.on_event("leave_room", self.handle_leave_room_event)
        socketio.on_event("clientmsg", self.handle_my_custom_event)

    @route("/landingpage", endpoint="landingpage")
    @route("/", endpoint="landingpage")
    def landingpage(self):
        return render_template("landingpage.html")

    @route("/profile", endpoint="profile",methods=["GET", "POST"])
    def profile(self):

        default_args = {"firstname" : session["firstname"], "lastname" : session["lastname"], "email": session["email"], "password": session["password"], "username": session["username"]}
        if request.method == "GET":
            return render_template("profile.html", **default_args)
        # the user can submit two types of post, change profile or change password.
        if "submit-profile" in request.form:

            form_email = request.form.get("email")
            form_username = request.form.get("username")
            current_user = ClientModel.query.filter_by(email=session['email']).first()
            email_exists = ClientModel.query.filter_by(email=form_email).all() != []
            username_exists = ClientModel.query.filter_by(username = form_username).all() != []
            if not email_exists:
                current_user.email = form_email
                session["email"] = form_email
                default_args["email"] = form_email
            else:
                # email exists.
                pass
            if not username_exists:
                current_user.username = form_username
                session["username"] = form_username
                default_args["username"] = form_username
            else:
                # username exists already
                pass
            default_args["email_exists"] = email_exists 
            default_args["username_exists"] = username_exists
        elif "submit-password" in request.form:
                old_password = Utility.EncryptSHA256(request.form.get("old-password"))
                new_password = Utility.EncryptSHA256(request.form.get("new-password-confirm"))
                # check if old password entry matches password in db.
                if old_password != session["password"]:
                    # HANDLE THIS
                    return "pw mismatch"
                ClientModel.query.filter_by(email=session['email']).first().password = new_password
                session["password"] = new_password
                default_args["password"] = new_password
        try:
            db.session.commit()
        except(Exception):
            pass
        return render_template("profile.html", **default_args)
        




    @route("/testing", endpoint="testing")
    def testing(self):
        return render_template("testing.html")
        
    @route("/", endpoint="/")
    @route("/login/", endpoint="login", methods=['POST', 'GET'])
    def login(self):
        if request.method == "GET":
            return render_template("landingpage.html")
        form_email = request.form.get("email")
        form_password = Utility.EncryptSHA256(request.form.get("password"))
        login_details = [form_email, form_password]
        for field in login_details:
            if not field:
                #todo handle this
                return render_template("login.html")
        user = ClientModel.query.filter_by(email=form_email, password=form_password).first()
        if  user == None:
            #todo handle this. Invalid login credentials.
            print("INVALID LOGIN CREDENTIALS")
            return render_template("landingpage.html")
        # optimise
        session["email"] = user.email
        session["username"] = user.username
        session["firstname"] = user.firstname
        session["lastname"] = user.lastname
        session["password"] = user.password
        session["active_session"] = ""
        return redirect("/profile")

    @route("/registration/",endpoint="registration", methods = ["GET", "POST"])
    def registration(self):
        if request.method == "GET":
            return render_template("registration.html")
        form_email = request.form.get("email")
        form_username = request.form.get("username")
        form_first_name = request.form.get("firstname")
        form_last_name = request.form.get("lastname")
        form_password = Utility.EncryptSHA256(request.form.get("password"))
        active_session = "0"
        data = [form_email, form_username,form_first_name,form_last_name,form_password, active_session]
        for field in data:
            if not field:
                #todo handle this
                return "404"
        user_exists = ClientModel.query.filter_by(email=form_email).first()
        if user_exists != None :
            #todo handle this. User is already registered.
            return "user exists already"
        db.session.add(ClientModel(username = form_username, firstname = form_first_name, lastname = form_last_name, email = form_email, password = form_password, active_session = "0"))
        db.session.commit()

        return redirect("/login")

    @route("/chat_logout/", endpoint="chat_logout")
    def chat_logout(self):
        session["active_session"] = None
        return redirect("/session")

    @route("/logout", endpoint="logout")
    def logout():
        session["email"] = None
        return redirect("/login")

    @route("/session", endpoint="session", methods=["GET", "POST"])
    def session(self):
        if request.method == "GET":
            return render_template("session.html")
        roomID = request.form.get("room")
        matchingRoomClients = ClientModel.query.filter_by(active_session = roomID).all()
        
        if "joinsession" in request.form:
            matchingRoomClients = ClientModel.query.filter_by(active_session = roomID).all()

            if matchingRoomClients == []:
                # handle this.
                return "room id does not exist"

        
        elif "createsession" in request.form:
            if matchingRoomClients != []:
                return "session id already exists"

        session["active_session"] = roomID
        ClientModel.query.filter_by(username = session["username"]).first().active_session = roomID
        db.session.commit()    
        return redirect(url_for("chat"))


    @route("/chat", endpoint="chat")
    def chat(self):
        username = session.get('username')
        room = session.get('active_session')
        if username and room:
            return render_template('chat.html', username=username, room=room)
        else:
            return redirect(url_for('session'))

    def handle_send_message_event(self,data):
        data["time"] = datetime.now().strftime("%H:%M")   
        data["username"] = session["username"]                                                         
        socketio.emit('receive_message',data, room=session['active_session'])


        


        
        message = Message(flairs = data["flairs"], upvotes = data["upvotes"], date = data["date"], messageID = data["messageID"])
         
        # store this object into our messages database.
        # construct a message object and store the message in a database.
        

    def handle_join_room_event(self,data):
        join_room(session['active_session'])
        data["time"] = datetime.now().strftime("[%H:%M]")
        data["username"] = session["username"]                                                            
        socketio.emit('join_room_announcement',data, room=session['active_session'], username=session["username"])

    def handle_leave_room_event(self,data):
        leave_room(session['active_session'])
        socketio.emit('leave_room_announcement', data, room=session['active_session'])


    def messageReceived(self,methods=['GET', 'POST']):
        print('message was received!!!')

    def handle_my_custom_event(self,json, methods=['GET', 'POST']):
        print('received my event: ' + str(json))
        socketio.emit('servermsg', json, callback=self.messageReceived)


    

JustAsk.register(app)