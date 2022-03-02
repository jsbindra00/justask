from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)

# The check same thread here is a temp fix to an error where the same object is used in different threads.
# https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
connect = sqlite3.connect('justaskdatabase.db', check_same_thread=False)
cursor = connect.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL);
    """)

# Save (commit) the changes
connect.commit()

@app.route('/')
def login():
    return render_template('testsite.html')


@app.route('/register', methods = ["GET", "POST"])
def register():
    
    if request.method == "GET":
        return render_template("register.html")

    # Get user submission
    username = request.form.get("username")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate submission
    data = [username,first_name,last_name,email,password]
    for field in data:
        if not field:
            #todo handle this
            return render_template("register.html")

    # If the user provided valid info, and they were not already registered, store data in database
    username_present = cursor.execute("SELECT * FROM users WHERE username= ?",(username,)).fetchall()
    if username_present != []:
        #todo handle this. User is already registered.
        return render_template("register.html")

    cursor.execute("INSERT INTO users VALUES (?,?,?,?, ?)", data)
    connect.commit()

    # maybe we should have a registration succesful page, that can then link to the login?
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    socketio.emit('receive_message',data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement',data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
