from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room
import sqlite3
from datetime import datetime


class Application:
    def __init__(self):
        
        self.CLIENT_SQL_INJECTION = """
            CREATE TABLE IF NOT EXISTS clients (
                clientJSON TEXT NOT NULL PRIMARY KEY);

            """


    
    def Start(self):

        # render and connect to the clientsdatabase.
        self.clientsDB = self.__ConnectToDatabase("clients.db")
        self.__InitialiseDatabase(self.clientsDB, self.CLIENT_SQL_INJECTION)



        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)

        # Configure session. Store on filesystem, and delete cookie when user closes browser.
        self.app.config["SESSION_PERMANENT"] = False
        self.app.config["SESSION_TYPE"] = "filesystem"
        Session(self.app)

        self.app.add_url_rule(rule="/", endpoint=None, view_func=self.profile)
        self.app.add_url_rule(rule="/", endpoint="profile", view_func=self.profile)
        self.app.add_url_rule(rule="/", endpoint="login", view_func=self.login, methods=["GET", "POST"])
        self.app.add_url_rule(rule="/", endpoint="chat_logout", view_func=self.chat_logout)
        self.app.add_url_rule(rule="/", endpoint="logout", view_func=self.logout)
        self.app.add_url_rule(rule="/", endpoint="register", view_func=self.register,methods = ["GET", "POST"])
        self.app.add_url_rule(rule="/", endpoint="chat_login", view_func=self.register,methods = ["GET", "POST"])
        self.app.add_url_rule(rule="/", endpoint="chat", view_func=self.register,methods = ["GET", "POST"])

        self.socketio.run(self.app, debug=True)




    def __ConnectToDatabase(self, dbName):
        connection =  None
        try:
            connection = sqlite3.connect(dbName, check_same_thread=False)
        except Exception as e:
            print("FAILED TO CONNECT TO DATABASE, ASSHOLE")
        return connection


    def __InitialiseDatabase(self, connectionObj, SQL_INJECTION):

        # pull the db interaction interface from the connection.
        self.cursor = connectionObj.cursor()

        # create the sql table in the db. 
            # we're just storing a single text column with 

        self.cursor.execute(SQL_INJECTION)
        connectionObj.commit()

    def profile(self):
        # If no user session, redirect to login page. Else render the user profile page.
        # if not session.get("email"):
        #     return redirect("/login")

        return render_template("profile.html")


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
        user = self.cursor.execute("SELECT * FROM users WHERE email= ? AND password = ?",(email, password)).fetchone()
        print("USER " + user)
        if  user == None:
            #todo handle this. Invalid login credentials.
            return render_template("login.html")

        session["email"] = user[0]
        session["username"] = user[1]
        session["first_name"] = user[2]
        session["last_name"] = user[2]
        session["role"] = user[4]

        return redirect("/profile")
        
    def chat_logout(self):
        session["room"] = None
        return redirect("/chat_login")

    def logout(self):
        session["email"] = None
        return redirect("/login")

    def register(self):
        if request.method == "GET":
            return render_template("register.html")

        # Get user submission

        email = request.form.get("email")
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        role = request.form.get("role")

        # Validate submission
        data = [email, username,first_name,last_name,password, role]
        for field in data:
            if not field:
                #todo handle this
                return render_template("register.html")

        # If the user provided valid info, and they were not already registered, store data in database
        email_present = self.cursor.execute("SELECT * FROM users WHERE email= ?",(email,)).fetchall()
        if email_present != []:
            #todo handle this. User is already registered.
            return render_template("register.html")

        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?, ?, ?)", data)
        self.clientsDB.commit()

        # maybe we should have a registration succesful page, that can then link to the login?
        return redirect("/login")


    def chat_login(self):
        if request.method == "GET":
            return render_template("chat_login.html")


        # store the session ID into a database consisting of active session ids.
        room = request.form.get("room")
        print("ROOM ",room)
        session["room"] = room

        return redirect(url_for("chat"))


    def chat(self):
        username = session.get('username')
        room = session.get('room')
        if username and room:
            return render_template('chat.html', username=username, room=room)
        else:
            return redirect(url_for('chat_login'))










def ValidateLoginDetails(clientObject):

    # no restrictions on first name and last name, should not be blank tho

    # username 
        # the username should not already be taken.

    # password
        # should be N characters long.
        # should contain a number.
        # should contain a capital letter.
    
    # email 
        # apply regex to the email, see what remains.

    


    return True








# @socketio.on('send_message')
# def handle_send_message_event(data):
#     app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
#                                                                     data['room'],
#                                                                     data['message']))
#     data["time"] = datetime.now().strftime("%H:%M")                                                               
#     socketio.emit('receive_message',data, room=data['room'])

    


# @socketio.on('join_room')
# def handle_join_room_event(data):
#     app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
#     join_room(data['room'])
#     data["time"] = datetime.now().strftime("[%H:%M]")
#     socketio.emit('join_room_announcement',data, room=data['room'])


# @socketio.on('leave_room')
# def handle_leave_room_event(data):
#     app.logger.info("{} has left the room {}".format(data['username'], data['room']))
#     leave_room(data['room'])
#     socketio.emit('leave_room_announcement', data, room=data['room'])




if __name__ == '__main__':
    application = Application()
    application.Start()
    print("good")
