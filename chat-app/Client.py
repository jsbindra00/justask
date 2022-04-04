from SharedContext import db
from ModelBase import ModelBase
from enum import IntEnum

class ClientAttribute(IntEnum):
    EMAIL=0
    USERNAME=1
    FIRSTNAME=2
    LASTNAME=3
    PASSWORD=4
    ACTIVE_SESSION=5
    ADMIN=6
    PROFILE_PICTURE = 7
    INSTAGRAM_PAGE=8
    TWITTER_PAGE=9
    FACEBOOK_PAGE=10
    LINKEDIN_PAGE=11
    ABOUT_ME = 12

class ClientModel(db.Model, ModelBase):

    __bind_key__ = "clients"

    EMAIL = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    USERNAME = db.Column(db.String(80), unique=True, nullable=False)
    FIRSTNAME = db.Column(db.String(80), unique=False, nullable=False)
    LASTNAME = db.Column(db.String(80), unique=False, nullable=False)
    PASSWORD = db.Column(db.String(80), unique=False, nullable=False)
    ACTIVE_SESSION = db.Column(db.String(80), unique=False, nullable=False)
    ADMIN = db.Column(db.Integer, unique=False, nullable=False)
    PROFILE_PICTURE = db.Column(db.String(80), unique=False, nullable=False)
    INSTAGRAM_PAGE = db.Column(db.String(80), unique=False, nullable=False)
    TWITTER_PAGE = db.Column(db.String(80), unique=False, nullable=False)
    FACEBOOK_PAGE = db.Column(db.String(80), unique=False, nullable=False)
    LINKEDIN_PAGE = db.Column(db.String(80), unique=False, nullable=False)
    ABOUT_ME = db.Column(db.String(120), unique=False, nullable=False, primary_key=False)



    def __repr__(self):
        return 'CLIENT {} {} {} {} {} {}'.format(self.email, self.username, self.firstname, self.lastname, self.password, self.active_session)
    def __init__(self, **kwargs):
        super(ClientModel, self).__init__(**kwargs)

    
    def SaveDatabase(filePath):
        # pull all clients.
        ModelBase.ProcessDatabase(ClientModel.query.all(), filePath)
        print("SAVED CLIENTS DB TO {}".format(filePath))
    