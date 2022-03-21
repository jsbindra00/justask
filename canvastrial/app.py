from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room
import sqlite3
from datetime import datetime


app = Flask(__name__)
socketio = SocketIO(app)

# Configure session. Store on filesystem, and delete cookie when user closes browser.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# The check same thread here is a temp fix to an error where the same object is used in different threads.
# https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
connect = sqlite3.connect('justaskdatabase.db', check_same_thread=False)
cursor = connect.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT NOT NULL PRIMARY KEY,
        username TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL);
    """)


cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        email TEXT NOT NULL PRIMARY KEY,
        message TEXT NOT NULL,
        username TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT NOT NULL);
    """)

# Save (commit) the changes
connect.commit()
class Application:
    def __init__(self):
        pass

@app.route('/')
@app.route('/profile')
def profile():
    # If no user session, redirect to login page. Else render the user profile page.
    if not session.get("email"):
        return redirect("/login")

    return render_template("profile.html")


@app.route('/login', methods = ["GET", "POST"])
def login():
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
        return render_template("login.html")

    session["email"] = user[0]
    session["username"] = user[1]
    session["first_name"] = user[2]
    session["last_name"] = user[2]
    session["role"] = user[4]

    return redirect("/profile")

@app.route("/chat_logout")
def chat_logout():
    session["room"] = None
    return redirect("/chat_login")

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/login")

@app.route('/register', methods = ["GET", "POST"])
def register():
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
    email_present = cursor.execute("SELECT * FROM users WHERE email= ?",(email,)).fetchall()
    if email_present != []:
        #todo handle this. User is already registered.
        return render_template("register.html")

    cursor.execute("INSERT INTO users VALUES (?,?,?,?, ?, ?)", data)
    connect.commit()

    # maybe we should have a registration succesful page, that can then link to the login?
    return redirect("/login")


@app.route('/chat_login' , methods = ["GET", "POST"])
def chat_login():
    print("HERE")
    if request.method == "GET":
        return render_template("chat_login.html")

    room = request.form.get("room")
    print("ROOM ",room)
    session["room"] = room

    return redirect(url_for("chat"))


@app.route('/chat', methods = ["GET", "POST"])
def chat():
    username = session.get('username')
    room = session.get('room')
    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('chat_login'))


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data["time"] = datetime.now().strftime("%H:%M")                                                               
    socketio.emit('receive_message',data, room=data['room'])

    


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    data["time"] = datetime.now().strftime("[%H:%M]")
    socketio.emit('join_room_announcement',data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])




def ValidateSessionID():

    pass

if __name__ == '__main__':
    socketio.run(app, debug=True)
