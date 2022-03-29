from app import clientsDB
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

class ClientModel(clientsDB.Model, ModelBase):

    email = clientsDB.Column(clientsDB.String(120), unique=True, nullable=False, primary_key=True)
    username = clientsDB.Column(clientsDB.String(80), unique=True, nullable=False)
    firstname = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    lastname = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    password = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)
    active_session = clientsDB.Column(clientsDB.String(80), unique=False, nullable=False)

    def __repr__(self):
        return 'CLIENT {} {} {} {} {} {}'.format(self.email, self.username, self.firstname, self.lastname, self.password, self.active_session)
    def __init__(self, **kwargs):
        super(ClientModel, self).__init__(**kwargs)

    def __ProcessDatabase(clients,filePath):
        f = open(filePath, "w")
        for client in clients:
            f.write(repr(client) + "\n")
        f.close()

    
    def SaveDatabase(filePath):
        # pull all clients.
        ClientModel.__ProcessDatabase(ClientModel.query.all(), filePath)
        all_users = ClientModel.query.all()
        ClientModel.__ProcessDatabase(all_users, filePath)
        print("SAVED CLIENTS DB TO {}".format(filePath))
    








