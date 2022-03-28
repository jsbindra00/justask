from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import clientsDB
from enum import IntEnum

class ClientAttribute(IntEnum):
    Email=0
    Username=1
    Firstname=2
    Lastname=3
    Password=4
    ActiveSession=5
    Admin=6

class ClientModel(clientsDB.Model):

    email = clientsDB.Column(clientsDB.String(120), unique=True, nullable=False, primary_key=True)
    username = clientsDB.Column(clientsDB.String(80), unique=True, nullable=False)
    firstname = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    lastname = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    password = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    active_session = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    def __init__(self, **kwargs):
        super(ClientModel, self).__init__(**kwargs)








