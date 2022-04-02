from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os



dbFilepath = "./"

testing = False
if testing:
    clientsDBLeaf = "\clients_test.db"
    messagesDBLeaf = "\messages_test.db"
else:
    clientsDBLeaf = "\clients.db"
    messagesDBLeaf = "\messages.db"

clientsDB = dbFilepath + clientsDBLeaf
messagesDB = dbFilepath + messagesDBLeaf





app = Flask(__name__)


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + clientsDB
SQLALCHEMY_BINDS = {
    'clients' : 'sqlite:///' + clientsDB,
    'messages' : 'sqlite:///' + messagesDB
}




# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS

options = {
}
socketio = SocketIO(app)
db = SQLAlchemy(app, session_options=options)





