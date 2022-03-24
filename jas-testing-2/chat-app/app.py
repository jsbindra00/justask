from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room
import sqlite3
from datetime import datetime
from flask_classful import FlaskView, route

app = Flask(__name__)
socketio = SocketIO(app)

dbName = "clients.db"
CLIENT_SQL_INJECTION = """
    CREATE TABLE IF NOT EXISTS users (
        email TEXT NOT NULL PRIMARY KEY,
        username TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        password TEXT NOT NULL,
        active_session TEXT NOT NULL);
    """
connection = sqlite3.connect(dbName, check_same_thread=False)

cursor = connection.cursor()
cursor.execute(CLIENT_SQL_INJECTION)
connection.commit()  

class JustAsk(FlaskView):
    default_methods = ['GET', 'POST']
    route_base = "/"
    def __init__(self):

        pass
    def Start(self):
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_TYPE"] = "filesystem"
        Session(app)

        socketio.on_event("send_message", self.handle_send_message_event)
        socketio.on_event("join_room", self.handle_join_room_event)
        socketio.on_event("leave_room", self.handle_leave_room_event)


    @route("/landingpage", endpoint="landingpage")
    @route("/", endpoint="landingpage")
    def landingpage(self):
        return render_template("landingpage.html")

    # @route("/", endpoint="/")
    @route("/profile", endpoint="profile",methods=["GET", "POST"])
    def profile(self):
        # If no user session, redirect to login page. Else render the user profile page.
        if not session.get("email"):
            return redirect("/login")
        return render_template("profile.html")

    @route("/", endpoint="/")
    @route("/login/", endpoint="login", methods=['POST', 'GET'])
    def login(self):
        if request.method == "GET":
            return render_template("login.html")

        # Get user login details
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate submission
        login_details = [email, password]
        for field in login_details:
            if not field:
                #todo handle this
                return render_template("login.html")
        # If the user provided details stored in the database, add these details to the session, 
        # and send them to their profile page
        user = cursor.execute("SELECT * FROM users WHERE email= ? AND password = ?",(email, password)).fetchone()
        print(user)
        if  user == None:
            #todo handle this. Invalid login credentials.
            print("INVALID LOGIN CREDENTIALS")
            return render_template("login.html")

        session["email"] = user[0]
        session["username"] = user[1]
        session["firstname"] = user[2]
        session["lastname"] = user[3]
        session["password"] = user[4]
        session["active_session"] = ""

        return redirect("/profile")





    @route("/registration/",endpoint="registration", methods = ["GET", "POST"])
    def registration(self):
        if request.method == "GET":
            return render_template("registration.html")

        # Get user submission
        email = request.form.get("email")
        username = request.form.get("username")
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        password = request.form.get("password")
        active_session = ""


        data = [email, username,first_name,last_name,password, active_session]
        for field in data:
            if not field:
                #todo handle this
                return render_template("404.html")


        # If the user provided valid info, and they were not already registered, store data in database
        email_present = cursor.execute("SELECT * FROM users WHERE email= ?",(email,)).fetchall()
        if email_present != []:
            #todo handle this. User is already registered.
            return render_template("userexists.html")

        cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", data)
        connection.commit()

        # maybe we should have a registration succesful page, that can then link to the login?
        return redirect("/login")


    @route("/chat_logout/", endpoint="chat_logout")
    def chat_logout(self):
        session["room"] = None
        return redirect("/newsession")


    @route("/logout", endpoint="logout")
    def logout():
        session["email"] = None
        return redirect("/login")


    @route("/joinsession", endpoint="joinsession", methods = ["GET", "POST"])
    def joinsession(self):
        # need to validate the session id string.
        if request.method == "GET":
            return render_template("joinsession.html")

        roomID = request.form.get("room")
        roomIDExists = cursor.execute("SELECT * FROM users WHERE active_session= ?",(roomID,)).fetchall()
        if roomIDExists != []:
            return "room id does not exist"

        sql_update_query = "UPDATE set active_session from users where " + " = 10000 where id = 4"

        # fetch the username for the current user.
        sql_update_query = "UPDATE set active_session = " + roomID + " where " 
    
        cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", roomID)
        connection.commit()


        print("ROOM ",roomID)
        session["room"] = roomID

        return redirect(url_for("chat"))




    @route("/newsession", endpoint="newsession")
    def newsession(self):
        return redirect(url_for("joinsession"))

    @route("/chat", endpoint="chat")
    def chat(self):
        username = session.get('username')
        room = session.get('room')
        if username and room:
            return render_template('chat.html', username=username, room=room)
        else:
            return redirect(url_for('newsession'))

    def handle_send_message_event(self,data):
        app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                        data['room'],
                                                                        data['message']))
        data["time"] = datetime.now().strftime("%H:%M")                                                               
        socketio.emit('receive_message',data, room=data['room'])

    def handle_join_room_event(self,data):
        app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
        join_room(data['room'])
        data["time"] = datetime.now().strftime("[%H:%M]")
        socketio.emit('join_room_announcement',data, room=data['room'])

    def handle_leave_room_event(self,data):
        app.logger.info("{} has left the room {}".format(data['username'], data['room']))
        leave_room(data['room'])
        socketio.emit('leave_room_announcement', data, room=data['room'])



JustAsk.register(app)

if __name__ == '__main__':
    application = JustAsk()
    application.Start()
    socketio.run(app, debug=True)

