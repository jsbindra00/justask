from math import perm
import unittest
from SharedContext import socketio, app, db
from flask_session import Session
from JustAsk import *
from Utility import Utility
from Client import ClientModel
from Message import MessageModel
import itertools

from flask import render_template, request, redirect, url_for, session
from flask_session import Session
from flask_classful import FlaskView, route
from Client import ClientModel
from Utility import Utility
from SharedContext import *
from Client import ClientAttribute

class FlaskTest_LandPage(unittest.TestCase):

    def setUp(self):

        # URLs
        self.HOME_URL = "http://127.0.0.1:5000/"
        self.LANDPAGE_URL = self.HOME_URL + "landingpage"
        self.REGISTER_URL = self.HOME_URL + "registration"
        self.LOGIN_URL = self.HOME_URL + "login"
        self.PROFILE_URL= self.HOME_URL + "profile"

        #setup application

        Session()
        self.application = JustAsk()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        #self.application.Start()
        app.testing = True
        self.client = app.test_client()

        #JustAsk.register(app)
    
        self.setup_data = dict(email='JohnSmith12@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password = 'Password1234')
        self.admin_client = ClientModel(EMAIL='JohnSmith12@gmail.com', FIRSTNAME='John', LASTNAME = 'Smith', USERNAME = 'John12', PASSWORD =  Utility.EncryptSHA256('Password1234'),
         ACTIVE_SESSION = '', ADMIN = 0, PROFILE_PICTURE = '', INSTAGRAM_PAGE = '', TWITTER_PAGE = '', FACEBOOK_PAGE = '', LINKEDIN_PAGE = '')
        db.session.add(self.admin_client)
        db.session.commit()

        self.test_data = dict(email='Correct12@gmail.com', firstname='Corr', lastname = 'Ect', username = 'Correct12', password = 'CorrectPassword1234')
    
    # test getting all routes works
    def test_get(self):
        response = self.client.get(self.HOME_URL)
        assert response.status_code == 200
    
    def test_register_user_with_correct_details(self):
        # email should start of not being in db
        email_present = ClientModel.query.filter_by(EMAIL=self.test_data["email"]).first()
        assert email_present is None

        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.REGISTER_URL + "/", data= self.test_data)
        email_present = ClientModel.query.filter_by(EMAIL=self.test_data["email"]).first()
        assert email_present is not None
        assert r.location == self.PROFILE_URL
    
    def test_registration_dublicate_email(self):
        # email should start of not being in db
        users = [self.setup_data, self.test_data]
        perm_list = [seq for seq in itertools.product([0,1], repeat=4)]
        test_data_dict = {}
        for order in perm_list:
            test_data_dict["email"] = self.setup_data["email"]
            test_data_dict["firstname"] = users[order[0]]["firstname"]
            test_data_dict["lastname"] = users[order[1]]["lastname"]
            test_data_dict["username"] = users[order[2]]["username"]
            test_data_dict["password"] = users[order[3]]["password"]
            r = self.client.post(self.REGISTER_URL + "/", data= test_data_dict)
            rows = db.session.query(ClientModel).count()
            assert rows == 1
            assert r.location == self.LANDPAGE_URL
            test_data_dict = {}

    def test_registration_dublicate_username(self):
        # email should start of not being in db
        users = [self.setup_data, self.test_data]
        perm_list = [seq for seq in itertools.product([0,1], repeat=4)]
        test_data_dict = {}
        for order in perm_list:
            test_data_dict["email"] = users[order[2]]["email"]
            test_data_dict["firstname"] = users[order[0]]["firstname"]
            test_data_dict["lastname"] = users[order[1]]["lastname"]
            test_data_dict["username"] = self.setup_data["username"]
            test_data_dict["password"] = users[order[3]]["password"]
            r = self.client.post(self.REGISTER_URL + "/", data= test_data_dict)
            rows = db.session.query(ClientModel).count()
            assert rows == 1
            assert r.location == self.LANDPAGE_URL
            test_data_dict = {}

    def test_registeration_empty_fields(self):
        empty_test_data = dict(email='', firstname='', lastname = '', username = '', password = '')
        users = [self.test_data, empty_test_data]
        perm_list = [seq for seq in itertools.product([0,1], repeat=5)]
        perm_list.remove((0,0,0,0,0))
        test_data_dict = {}
        for order in perm_list:
            test_data_dict["email"] = users[order[0]]["email"]
            test_data_dict["firstname"] = users[order[1]]["firstname"]
            test_data_dict["lastname"] = users[order[2]]["lastname"]
            test_data_dict["username"] = users[order[3]]["username"]
            test_data_dict["password"] = users[order[4]]["password"]
            r = self.client.post(self.REGISTER_URL + "/", data= test_data_dict)
            rows = db.session.query(ClientModel).count()
            assert rows == 1
            assert r.location == self.LANDPAGE_URL
            test_data_dict = {}

    def test_registration_incorrect_email_formats(self):
        email_test_data = dict(email=None, firstname='pass', lastname = 'test', username = 'usernamepass', password = "pN2baA1password")
        
        failure_start = [".johnny@mail.com", "/coin@kort.co.uk", "-main@main.com"]
        failure_at = ["usermail.com", "origincompany.co.uk"]
        failure_no_start = ["@right.com", "@optimal.co.uk"]
        failure_no_end = ["morning", "morning@", "morning@company", "morning@company.", "name@.com"]

        for case in failure_start:
            email_test_data["email"] = case
            r = self.client.post(self.REGISTER_URL + "/", data= email_test_data)
            email_present = ClientModel.query.filter_by(EMAIL=email_test_data["email"]).first()
            assert email_present is None
            assert r.location == self.LANDPAGE_URL
        
        for case in failure_at:
            email_test_data["email"] = case
            r = self.client.post(self.REGISTER_URL + "/", data= email_test_data)
            email_present = ClientModel.query.filter_by(EMAIL=email_test_data["email"]).first()
            assert email_present is None
            assert r.location == self.LANDPAGE_URL
        
        for case in failure_no_start:
            email_test_data["email"] = case
            r = self.client.post(self.REGISTER_URL + "/", data= email_test_data)
            email_present = ClientModel.query.filter_by(EMAIL=email_test_data["email"]).first()
            assert email_present is None
            assert r.location == self.LANDPAGE_URL
        
        for case in failure_no_end:
            email_test_data["email"] = case
            r = self.client.post(self.REGISTER_URL + "/", data= email_test_data)
            email_present = ClientModel.query.filter_by(EMAIL=email_test_data["email"]).first()
            assert email_present is None
            assert r.location == self.LANDPAGE_URL


    def test_registration_incorrect_password_formats(self):
        password_test_data = dict(email='passwordtesting@gmail.com', firstname='pass', lastname = 'test', username = 'usernamepass', password = None)
        email_present = ClientModel.query.filter_by(EMAIL=password_test_data["email"]).first()
        assert email_present is None

        failure_length = [" ",
        "a", "1", "A",
        "ab", "a1", "aA", "A1", "AB", "12",
        "aA1", "baA1", "2baA1", "N2baA1", "pN2baA1"]
        failure_no_number = ["passworDwithLength", "onetwoThreeFour"]
        failure_no_capital = ["passwordwith1ength", "cap1talletter"]
        failure_no_lower = ["A11CAPITAL", "CAPSL0CK"]

        for case in failure_length:
            password_test_data["password"] = case
            r = self.client.post(self.REGISTER_URL + "/", data= password_test_data)
            email_present = ClientModel.query.filter_by(EMAIL=password_test_data["email"]).first()
            assert email_present is None
            assert r.location == self.LANDPAGE_URL

        for case in failure_no_number:
            password_test_data["password"] = case
            r = self.client.post(self.REGISTER_URL + "/", data= password_test_data)
            email_present = ClientModel.query.filter_by(EMAIL=password_test_data["email"]).first()
            assert email_present is None
            assert r.location == self.LANDPAGE_URL

        for case in failure_no_capital:
            password_test_data["password"] = case
            r = self.client.post(self.REGISTER_URL + "/", data= password_test_data)
            email_present = ClientModel.query.filter_by(EMAIL=password_test_data["email"]).first()
            assert email_present is None
            assert r.location == self.LANDPAGE_URL

        for case in failure_no_lower:
            password_test_data["password"] = case
            r = self.client.post(self.REGISTER_URL + "/", data= password_test_data)
            email_present = ClientModel.query.filter_by(EMAIL=password_test_data["email"]).first()
            assert email_present is None
            assert r.location == self.LANDPAGE_URL

    #     # Registeration didnt have validation implemented debug

    def test_login(self):
        # email should start of not being in db
        login_cred = dict(email=self.setup_data["email"],password=self.setup_data["password"])
        email_present = ClientModel.query.filter_by(EMAIL=login_cred["email"]).first()
        assert email_present is not None

        # after post, user should be redirected, and data should be present in db=
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location == self.PROFILE_URL

    def test_login_incorrect_email(self):
        # email should start of not being in db
        login_cred = dict(email=self.test_data["email"],password=self.setup_data["password"])
        email_present = ClientModel.query.filter_by(EMAIL=login_cred["email"]).first()
        assert email_present is None

        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location is None

    def test_login_incorrect_password(self):
        # email should start of not being in db
        login_cred = dict(email=self.setup_data["email"],password=self.test_data["password"])
        email_present = ClientModel.query.filter_by(EMAIL=login_cred["email"]).first()
        assert email_present is not None

        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location is None

    def test_login_incorrect_credentials(self):
        # email should start of not being in db
        login_cred = dict(email=self.test_data["email"],password=self.test_data["password"])
        email_present = ClientModel.query.filter_by(EMAIL=login_cred["email"]).first()
        assert email_present is None

        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location is None
    
    def test_login_empty_email(self):
        # email should start of not being in db
        login_cred = dict(email="",password=self.setup_data["password"])
        email_present = ClientModel.query.filter_by(EMAIL=login_cred["email"]).first()
        assert email_present is None

        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location is None

    def test_login_empty_password(self):
        # email should start of not being in db
        login_cred = dict(email=self.setup_data["email"],password="")
        email_present = ClientModel.query.filter_by(EMAIL=login_cred["email"]).first()
        assert email_present is not None

        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location is None

    def test_login_empty_credentials(self):
        # email should start of not being in db
        login_cred = dict(email="",password="")
        email_present = ClientModel.query.filter_by(EMAIL=login_cred["email"]).first()
        assert email_present is None

        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location is None
    
    def test_register_login(self):
        r = self.client.post(self.REGISTER_URL + "/", data= self.test_data)
        email_present = ClientModel.query.filter_by(EMAIL=self.test_data["email"]).first()
        assert email_present is not None
        assert r.location == self.PROFILE_URL

        login_cred = dict(email=self.test_data["email"],password=self.test_data["password"])
        email_present = ClientModel.query.filter_by(EMAIL=login_cred["email"]).first()
        assert email_present is not None

        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location == self.PROFILE_URL

    # remove the setup data from db
    def tearDown(self):
        #db.session.remove()
        db.drop_all()
        self.app_context.pop()
        

class FlaskTest_Profile(unittest.TestCase):
    
    def setUp(self):
        # URLs
        self.HOME_URL = "http://127.0.0.1:5000/"
        self.LANDPAGE_URL = self.HOME_URL + "landingpage"
        self.REGISTER_URL = self.HOME_URL + "registration"
        self.LOGIN_URL = self.HOME_URL + "login"
        self.PROFILE_URL= self.HOME_URL + "profile"

        #setup application

        Session()
        self.application = JustAsk()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        #self.application.Start()
        app.testing = True
        self.client = app.test_client()

        # initialise user to perform tests on
        self.setup_data = dict(email='JohnSmith12@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password = 'Password1234')
        self.setup_data_client =  ClientModel(EMAIL='JohnSmith12@gmail.com', FIRSTNAME='John', LASTNAME = 'Smith', USERNAME = 'John12', PASSWORD =  Utility.EncryptSHA256('Password1234'),
         ACTIVE_SESSION = '', ADMIN = 0, PROFILE_PICTURE = '', INSTAGRAM_PAGE = '', TWITTER_PAGE = '', FACEBOOK_PAGE = '', LINKEDIN_PAGE = '')
        db.session.add(self.setup_data_client)
        db.session.commit()
        login_cred = dict(email=self.setup_data["email"],password=self.setup_data["password"])
        self.client.post(self.LOGIN_URL + "/", data= login_cred)

        # login_cred = dict(email=self.setup_data["email"],password=self.setup_data["password"])
        # r = self.client.post(self.LOGIN_URL, data= login_cred)

    def test_change_profile_info(self):
        # User logs into profile page, and wants to change email to a new one.
        with self.client:
            data = {"firstname" : "Jan", "lastname" : "Ponds", "email"  : "ab@gmail.com", "username" : 'JP', "submit-profile" : ""}
            #empty_test_data = {"firstname" : "", "lastname" : "", "email"  : "", "username" : '', "submit-profile" : ""}
            users = [data, self.setup_data]
            perm_list = [seq for seq in itertools.product([0,1], repeat=5)]
            test_data_dict = {}
            for order in perm_list:
                test_data_dict["EMAIL"] = users[order[0]]["email"]
                test_data_dict["FIRSTNAME"] = users[order[1]]["firstname"]
                test_data_dict["LASTNAME"] = users[order[2]]["lastname"]
                test_data_dict["USERNAME"] = users[order[3]]["username"]
                test_data_dict["submit-profile"] = ""
                r = self.client.post(self.PROFILE_URL, data= test_data_dict)
                assert session["EMAIL"] == users[order[0]]["email"]
                assert session["FIRSTNAME"] == users[order[1]]["firstname"]
                assert session["LASTNAME"] == users[order[2]]["lastname"]
                assert session["USERNAME"] == users[order[3]]["username"]
                test_data_dict = {}
    
    def test_change_email_username_dublication(self):
        with self.client:
            test_data = dict(email='Correct12@gmail.com', firstname='Corr', lastname = 'Ect', username = 'Correct12', password = 'CorrectPassword1234')
            r = self.client.post(self.REGISTER_URL + "/", data= test_data)
            email_present = ClientModel.query.filter_by(EMAIL=test_data["email"]).first()
            assert email_present is not None
            assert r.location == self.PROFILE_URL

            profile_change = {"FIRSTNAME" : "", "LASTNAME" : "", "EMAIL"  : "", "USERNAME" : '', "submit-profile" : ""}
            profile_change["EMAIL"] = self.setup_data["email"]
            self.client.post(self.PROFILE_URL, data= profile_change)
            assert session["EMAIL"] == test_data["email"]
            assert session["FIRSTNAME"] == test_data["firstname"]
            assert session["LASTNAME"] == test_data["lastname"]
            assert session["USERNAME"] == test_data["username"]
            profile_change["EMAIL"] = ""
            profile_change["USERNAME"] = self.setup_data["username"]
            self.client.post(self.PROFILE_URL, data= profile_change)
            assert session["EMAIL"] == test_data["email"]
            assert session["FIRSTNAME"] == test_data["firstname"]
            assert session["LASTNAME"] == test_data["lastname"]
            assert session["USERNAME"] == test_data["username"]

    def test_empty_fields_profile_change(self):
        with self.client:
            empty_test_data = {"FIRSTNAME" : "", "LASTNAME" : "", "EMAIL"  : "", "USERNAME" : '', "submit-profile" : ""}
            r = self.client.post(self.PROFILE_URL, data= empty_test_data)
            assert session["EMAIL"] == self.setup_data["email"]
            assert session["FIRSTNAME"] == self.setup_data["firstname"]
            assert session["LASTNAME"] == self.setup_data["lastname"]
            assert session["USERNAME"] == self.setup_data["username"]
    
    def test_change_invalid_email(self):
        failure_start = [".johnny@mail.com", "/coin@kort.co.uk", "-main@main.com"]
        failure_at = ["usermail.com", "origincompany.co.uk"]
        failure_no_start = ["@right.com", "@optimal.co.uk"]
        failure_no_end = ["morning", "morning@", "morning@company", "morning@company.", "name@.com"]
        with self.client:
            test_data = {"FIRSTNAME" : "", "LASTNAME" : "", "EMAIL"  : "", "USERNAME" : '', "submit-profile" : ""}
            for case in failure_start:
                test_data["EMAIL"] = case
                r = self.client.post(self.PROFILE_URL, data= test_data)
                assert session["EMAIL"] == self.setup_data["email"]
            
            for case in failure_at:
                test_data["EMAIL"] = case
                r = self.client.post(self.PROFILE_URL, data= test_data)
                assert session["EMAIL"] == self.setup_data["email"]
            
            for case in failure_no_start:
                test_data["EMAIL"] = case
                r = self.client.post(self.PROFILE_URL, data= test_data)
                assert session["EMAIL"] == self.setup_data["email"]
            
            for case in failure_no_end:
                test_data["EMAIL"] = case
                r = self.client.post(self.PROFILE_URL, data= test_data)
                assert session["EMAIL"] == self.setup_data["email"]

    def test_change_password(self):
        with self.client:
            test_data = {"old-password" : self.setup_data["password"], "new-password" : "NewPassword123", "new-password-confirm" : "NewPassword123", "submit-password" : ""}
            response = self.client.post(self.PROFILE_URL, data = test_data)
            assert session["PASSWORD"] == Utility.EncryptSHA256(test_data["new-password"])
            test_data["old-password"] = test_data["new-password"]
            test_data["new-password"] = "New12310testing"
            test_data["new-password-confirm"] = "New12310testing"
            response = self.client.post(self.PROFILE_URL, data = test_data)
            assert session["PASSWORD"] == Utility.EncryptSHA256(test_data["new-password"])
    
    def test_change_false_old_password(self):
        with self.client:
            test_data = {"old-password" : "FalsePassword123", "new-password" : "NewPassword123", "new-password-confirm" : "NewPassword123", "submit-password" : ""}
            response = self.client.post(self.PROFILE_URL, data = test_data)
            assert session["PASSWORD"] == Utility.EncryptSHA256(self.setup_data["password"])

    def test_change_false_confirmation_password(self):
        with self.client:
            test_data = {"old-password" : self.setup_data["password"], "new-password" : "NewPassword123", "new-password-confirm" : "FalseConfirm123", "submit-password" : ""}
            response = self.client.post(self.PROFILE_URL, data = test_data)
            assert session["PASSWORD"] == Utility.EncryptSHA256(self.setup_data["password"])
    
    def test_change_invalid_password(self):
        failure_length = ["", " ",
        "a", "1", "A",
        "ab", "a1", "aA", "A1", "AB", "12",
        "aA1", "baA1", "2baA1", "N2baA1", "pN2baA1"]
        failure_no_number = ["passworDwithLength", "onetwoThreeFour"]
        failure_no_capital = ["passwordwith1ength", "cap1talletter"]
        failure_no_lower = ["A11CAPITAL", "CAPSL0CK"]

        test_data = {"old-password" : self.setup_data["password"], "new-password" : "", "new-password-confirm" : "", "submit-password" : ""}
        with self.client:
            for case in failure_length:
                test_data["new-password"] = case
                test_data["new-password-confirm"] = case
                response = self.client.post(self.PROFILE_URL, data = test_data)
                assert session["PASSWORD"] == Utility.EncryptSHA256(self.setup_data["password"])

            for case in failure_no_number:
                test_data["new-password"] = case
                test_data["new-password-confirm"] = case
                response = self.client.post(self.PROFILE_URL, data = test_data)
                assert session["PASSWORD"] == Utility.EncryptSHA256(self.setup_data["password"])

            for case in failure_no_capital:
                test_data["new-password"] = case
                test_data["new-password-confirm"] = case
                response = self.client.post(self.PROFILE_URL, data = test_data)
                assert session["PASSWORD"] == Utility.EncryptSHA256(self.setup_data["password"])

            for case in failure_no_lower:
                test_data["new-password"] = case
                test_data["new-password-confirm"] = case
                response = self.client.post(self.PROFILE_URL, data = test_data)
                assert session["PASSWORD"] == Utility.EncryptSHA256(self.setup_data["password"])
    
    def test_register_change_profile(self):
        test_data = dict(email='Correct12@gmail.com', firstname='Corr', lastname = 'Ect', username = 'Correct12', password = 'CorrectPassword1234')
        r = self.client.post(self.REGISTER_URL + "/", data= test_data)
        email_present = ClientModel.query.filter_by(EMAIL=test_data["email"]).first()
        assert email_present is not None
        assert r.location == self.PROFILE_URL

        login_cred = dict(email=test_data["email"],password=test_data["password"])
        r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
        assert r.location == self.PROFILE_URL

        with self.client:
            profile_change = {"FIRSTNAME" : "Newton", "LASTNAME" : "Born", "EMAIL"  : "dollarnb@mail.co.uk", "USERNAME" : 'nb6', "submit-profile" : ""}
            self.client.post(self.PROFILE_URL, data= profile_change)
            assert session["EMAIL"] == profile_change["EMAIL"]
            assert session["FIRSTNAME"] == profile_change["FIRSTNAME"]
            assert session["LASTNAME"] == profile_change["LASTNAME"]
            assert session["USERNAME"] == profile_change["USERNAME"]
            password_change = {"old-password" : test_data["password"], "new-password" : "6NewestPassport", "new-password-confirm" : "6NewestPassport", "submit-password" : ""}
            self.client.post(self.PROFILE_URL, data = password_change)
            assert session["PASSWORD"] == Utility.EncryptSHA256(password_change["new-password"])

            login_cred = dict(email=profile_change["EMAIL"],password=password_change["new-password"])
            r = self.client.post(self.LOGIN_URL + "/", data= login_cred)
            assert r.location == self.PROFILE_URL
            assert session["EMAIL"] == profile_change["EMAIL"]
            assert session["FIRSTNAME"] == profile_change["FIRSTNAME"]
            assert session["LASTNAME"] == profile_change["LASTNAME"]
            assert session["USERNAME"] == profile_change["USERNAME"]
            assert session["PASSWORD"] == Utility.EncryptSHA256(password_change["new-password"])
        
    # remove the setup data from db
    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

# class FlaskTest_Sessions(unittest.TestCase):
    
#     def setUp(self):
#         # URLs
#         self.HOME_URL_CHECK = "http://127.0.0.1:5000"
#         self.REGISTER_URL_CHECK = "http://127.0.0.1:5000/registration"
#         self.LOGIN_URL_CHECK = "http://127.0.0.1:5000/login"
#         self.PROFILE_URL_CHECK= "http://127.0.0.1:5000/profile"
#         self.SESSION_URL_CHECK = "http://127.0.0.1:5000/session"
        
#         self.HOME_URL = "http://127.0.0.1:5000/"
#         self.REGISTER_URL = "http://127.0.0.1:5000/registration/"
#         self.LOGIN_URL = "http://127.0.0.1:5000/login/"
#         self.PROFILE_URL= "http://127.0.0.1:5000/profile/"

#         #setup application
#         Session()
#         self.application = JustAsk()
#         self.app_context = app.app_context()
#         self.app_context.push()
#         db.create_all()
#         self.application.Start()
#         app.testing = True
#         self.client = app.test_client()

#         # initialise user to perform tests on
#         self.setup_data = dict(email='JohnSmith12@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password = 'Password1234')
#         self.setup_data_b = dict(email='SamSmith12@gmail.com', firstname='Sam', lastname = 'Smith', username = 'Sam12', password = 'pasSword14')
#         self.setup_data_client = ClientModel(email='JohnSmith12@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password =  Utility.EncryptSHA256('password1234'), active_session = '0')
#         db.session.add(self.setup_data_client)
#         self.setup_data_client_b = ClientModel(email='SamSmith12@gmail.com', firstname='Sam', lastname = 'Smith', username = 'Sam12', password = Utility.EncryptSHA256('pasSword14'), active_session = '0')
#         db.session.add(self.setup_data_client_b)
#         db.session.commit()
#         login_cred = dict(email=self.setup_data["email"],password=self.setup_data["password"])
#         self.client.post(self.LOGIN_URL, data= login_cred)

#         # login_cred = dict(email=self.setup_data["email"],password=self.setup_data["password"])
#         # r = self.client.post(self.LOGIN_URL, data= login_cred)

#     def test_create_session(self):
#         test_data = {"room" : "room1", "createsession" : ""}
#         response = self.client.post(self.SESSION_URL_CHECK, data = test_data, follow_redirects=True)
#         assert session["active_session"] == test_data["active_session"]
#         test_data["room"] = "room2"
#         response = self.client.post(self.SESSION_URL_CHECK, data = test_data, follow_redirects=True)
#         assert session["active_session"] == test_data["active_session"]


#     def test_join_session(self):
#         test_data = {"room" : "room1", "createsession" : ""}
#         response = self.client.post(self.SESSION_URL_CHECK, data = test_data, follow_redirects=True)
#         assert session["active_session"] == test_data["active_session"]
#         test_data = {"room" : "room1", "joinsession" : ""}
#         response = self.client.post(self.SESSION_URL_CHECK, data = test_data, follow_redirects=True)
#         assert session["active_session"] == test_data["active_session"]

#         login_cred = dict(email=self.setup_data_b["email"],password=self.setup_data_b["password"])
#         self.client.post(self.LOGIN_URL, data= login_cred)

#         response = self.client.post(self.SESSION_URL_CHECK, data = test_data, follow_redirects=True)
#         assert session["active_session"] == test_data["active_session"]
    
#     def test_join_nonexistent_session(self):
#         test_data = {"room" : "room1", "joinsession" : ""}
#         response = self.client.post(self.SESSION_URL_CHECK, data = test_data, follow_redirects=True)
#         assert response.location == None
    
#     def test_create_same_session(self):
#         test_data = {"room" : "room1", "createsession" : ""}
#         response = self.client.post(self.SESSION_URL_CHECK, data = test_data, follow_redirects=True)
#         login_cred = dict(email=self.setup_data_b["email"],password=self.setup_data_b["password"])
#         self.client.post(self.LOGIN_URL, data= login_cred)
#         response = self.client.post(self.SESSION_URL_CHECK, data = test_data, follow_redirects=True)
#         assert response.location == None

#     # remove the setup data from db
#     def tearDown(self):
#         db.drop_all()
#         self.app_context.pop()

# class FlaskTest_Chat(unittest.TestCase):

#     def setUp(self):
#         # URLs
#         self.HOME_URL_CHECK = "http://127.0.0.1:5000"
#         self.REGISTER_URL_CHECK = "http://127.0.0.1:5000/registration"
#         self.LOGIN_URL_CHECK = "http://127.0.0.1:5000/login"
#         self.PROFILE_URL_CHECK = "http://127.0.0.1:5000/profile"
#         self.SESSION_URL_CHECK = "http://127.0.0.1:5000/session"
#         self.CHAT_URL_CHECK = "http://127.0.0.1:5000/chat"
        
#         self.HOME_URL = "http://127.0.0.1:5000/"
#         self.REGISTER_URL = "http://127.0.0.1:5000/registration/"
#         self.LOGIN_URL = "http://127.0.0.1:5000/login/"
#         self.PROFILE_URL= "http://127.0.0.1:5000/profile/"

#         #setup application
#         Session()
#         self.application = JustAsk()
#         self.app_context = app.app_context()
#         self.app_context.push()
#         db.create_all()
#         self.application.Start()
#         app.testing = True
#         self.client = app.test_client()

#         # initialise user to perform tests on
#         self.setup_data = dict(email='JohnSmith12@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password = 'password1234')
#         self.setup_data_client = ClientModel(email='JohnSmith12@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password =  Utility.EncryptSHA256('password1234'), active_session = '0')
#         db.session.add(self.setup_data_client)
#         db.session.commit()
#         login_cred = dict(email=self.setup_data["email"],password=self.setup_data["password"])
#         self.client.post(self.LOGIN_URL, data= login_cred)
#         self.client.post(self.SESSION_URL_CHECK, data = {"room" : "room1", "createsession" : ""}, follow_redirects=True)

#         # login_cred = dict(email=self.setup_data["email"],password=self.setup_data["password"])
#         # r = self.client.post(self.LOGIN_URL, data= login_cred)

#     def test_leave_room_event(self):
#         pass
    
#     def test_my_custom_event(self):
#         pass

#     def test_upvotes(self):
#         pass

#     def test_sent_messages(self):
#         test_data = {"chatbar" : "hello_world", "post" : ""}
#         self.client.post(self.CHAT_URL_CHECK, data = test_data)
#         data_check = MessageModel.query.filter_by(from_user=self.setup_data["username"]).first()
#         assert test_data["chatbar"] == data_check.payload

#     # remove the setup data from db
#     def tearDown(self):
#         db.drop_all()
#         self.app_context.pop()

if __name__ == "__main__":
    JustAsk.register(app)
    unittest.main()
