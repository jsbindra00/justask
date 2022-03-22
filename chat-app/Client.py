from enum import IntEnum
import json

class ClientAttribute(IntEnum):
    Username = 0
    Password = 1
    Email = 2
    OwnedSessions = 3
    JoinedSessions = 4
    FirstName = 5
    LastName = 6

class ClientDataBase:

    MAX_USERNAME_LENGTH = 20
    MAX_PASSWORD_LENGTH = 20
    MAX_EMAIL_LENGTH = 20
    




class JAClient:

    def __init__(self):
        self.attributes_ = {}
    
        self.RegisterAttribute(ClientAttribute.Username, None)
        self.RegisterAttribute(ClientAttribute.Password, None)
        self.RegisterAttribute(ClientAttribute.Email, None)
        self.RegisterAttribute(ClientAttribute.OwnedSessions, None)
        self.RegisterAttribute(ClientAttribute.JoinedSessions, None)
        self.RegisterAttribute(ClientAttribute.FirstName, None)


    def RegisterAttribute(self, attributeType, value):

        self.attributes_[attributeType] = value


    def LoadFromJSON(self, jsonString):

        attributes = {}
        # pull the attributes from the JSON string.
            # iterate through each attribute and convert each string attribute into the enum type in a new dictionary
        
        recreatedObject = json.loads(jsonString)
        clientAttributes = recreatedObject['attributes_']

        for key in clientAttributes:
            attributes[ClientAttribute(int(key))] = clientAttributes[key]
        self.attributes_ = attributes
        
      

        













