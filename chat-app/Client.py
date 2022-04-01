from SharedContext import db
from enum import IntEnum
from ModelBase import ModelBase

class ClientAttribute(IntEnum):
    Email=0
    Username=1
    Firstname=2
    Lastname=3
    Password=4
    ActiveSession=5
    Admin=6

class ClientModel(db.Model, ModelBase):

    __bind_key__ = "clients"

    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    active_session = db.Column(db.String(80), unique=False, nullable=False)


    def __repr__(self):
        return 'CLIENT {} {} {} {} {} {}'.format(self.email, self.username, self.firstname, self.lastname, self.password, self.active_session)
    def __init__(self, **kwargs):
        super(ClientModel, self).__init__(**kwargs)

    
    def SaveDatabase(filePath):
        # pull all clients.
        ModelBase.ProcessDatabase(ClientModel.query.all(), filePath)
        print("SAVED CLIENTS DB TO {}".format(filePath))
    








