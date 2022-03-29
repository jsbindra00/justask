from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os

file_path = os.path.abspath(os.getcwd())+"\clients.db"




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
socketio = SocketIO(app)

options = {
}

clientsDB = SQLAlchemy(app, session_options=options)
messageDB = SQLAlchemy(app, session_options=options)



