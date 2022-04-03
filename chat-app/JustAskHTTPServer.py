from multiprocessing.connection import Client
from flask import render_template, request, redirect, url_for, session
from flask_session import Session
from flask_classful import FlaskView, route
from Client import ClientModel
from Utility import Utility
from SharedContext import *
from Client import ClientAttribute



class JustAskHTTPServer(FlaskView):
    
    default_methods = ['GET', 'POST']
    route_base = "/"

    def __init__(self):
        super().__init__()

        db.create_all()
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_TYPE"] = "filesystem"
        Session(app)

    def UpdateSessionInformation(self, client_attribute, arg, updateDB = False, auto_commit = True):
        client_attribute = ClientAttribute(client_attribute)
        session[client_attribute.name] = arg

        if updateDB:
            # if we just replaced the username in our session, perform search by email.
            SEARCH_PRED = ClientAttribute(ClientAttribute.EMAIL if client_attribute == ClientAttribute.USERNAME else ClientAttribute.USERNAME)
            current_user = ClientModel.query.filter_by(**{SEARCH_PRED.name : session[SEARCH_PRED.name]}).first()
            setattr(current_user, client_attribute.name, arg)
            if auto_commit: db.session.commit()
    def GetUser(self, client_attributes):
        return ClientModel.query.filter_by(**client_attributes).first()

    def GetSessionInformation(self, client_attribute):
        return session[ClientAttribute(client_attribute).name]

    # This should be on SocketServer.py
    def KickUser(self, username):
        user = self.GetUser({ClientAttribute.USERNAME.name : username})
        if user is not None:
            user.ACTIVE_SESSION = ""
            user.ADMIN = 0
            
        return redirect("/profile")
    
    def IsUserLoggedIn(self):
        return session
    
    def CreateUser(self, user_information):
        user = ClientModel(**user_information)
        db.session.add(user)
        db.session.commit()
        return user

    def UserExists(self, username, email):
        return ClientModel.query.filter_by(EMAIL = email).first() != None or ClientModel.query.filter_by(USERNAME = username).first() != None

    @route("/signout", endpoint="signout")
    def ROUTE_SIGNOUT(self):
        if self.IsUserLoggedIn():session.clear()
        return redirect("/landingpage")

    @route("/landingpage", endpoint="landingpage")
    @route("/", endpoint="landingpage")
    def ROUTE_LANDING_PAGE(self):
        return redirect("profile") if self.IsUserLoggedIn() else render_template("landingpage.html")

    @route("/leave_session", endpoint="leave_session",methods=["POST", "GET"])
    def ROUTE_LEAVE_SESSION(self):
        if session["ACTIVE_SESSION"]: self.UpdateSessionInformation(ClientAttribute.ACTIVE_SESSION, "", updateDB=True)
        return redirect("/profile")
        
    @route("/testing", endpoint="testing")
    def ROUTE_TESTING(self):
        return render_template("testing.html")

    @route("/mcq", endpoint="mcq")
    def ROUTE_MCQ(self):
        return render_template("mcq.html")

    # def PROFILE_CHANGE_ASSIGNMENT(self, change_exists, client_attribute, form_input, default):
    #     if change_exists:
    #         print("oj")
    #         self.UpdateSessionInformation(client_attribute, form_input, updateDB=True) 
    #         return form_input
    #     return default
    def CHANGE_PROFILE_INFORMATION(self, default_args):
        # print("CHANGING PROFILE INFORMATION")
        # form_firstname = request.form.get("FIRSTNAME")
        # form_lastname = request.form.get("LASTNAME")
        # form_username = request.form.get("USERNAME")
        # form_email = request.form.get("EMAIL")

        # # I don't understand why these need to be stored
        # # The change I made is: If a change happened, then existence is true otherwise its false
        # default_args["FIRSTNAME_EXISTS"] = bool(form_firstname)
        # default_args["LASTNAME_EXISTS"] = bool(form_lastname)
        # default_args["USERNAME_EXISTS"] = bool(form_username) and ClientModel.query.filter_by(USERNAME = form_username).all() == []
        # default_args["EMAIL_EXISTS"] = bool(form_email) and ClientModel.query.filter_by(EMAIL = form_email).all() == [] and Utility.IsEmailAddress(form_email)
        
        # default_args[ClientAttribute.FIRSTNAME.name] = self.PROFILE_CHANGE_ASSIGNMENT(default_args["FIRSTNAME_EXISTS"], ClientAttribute.FIRSTNAME, form_firstname, default_args[ClientAttribute.FIRSTNAME.name])
        # default_args[ClientAttribute.LASTNAME.name] = self.PROFILE_CHANGE_ASSIGNMENT(default_args["LASTNAME_EXISTS"], ClientAttribute.LASTNAME, form_lastname, default_args[ClientAttribute.LASTNAME.name])
        # default_args[ClientAttribute.USERNAME.name] = self.PROFILE_CHANGE_ASSIGNMENT(default_args["USERNAME_EXISTS"], ClientAttribute.USERNAME, form_username, default_args[ClientAttribute.USERNAME.name])
        # default_args[ClientAttribute.EMAIL.name] = self.PROFILE_CHANGE_ASSIGNMENT(default_args["EMAIL_EXISTS"], ClientAttribute.EMAIL, form_email, default_args[ClientAttribute.EMAIL.name])

        # return default_args
        print("CHANGING PROFILE INFORMATION")
        form_email = request.form.get("EMAIL")
        print(form_email)
        email_exists = ClientModel.query.filter_by(EMAIL=form_email).all() != []
        if not email_exists:
            self.UpdateSessionInformation(ClientAttribute.EMAIL, form_email, updateDB=True)
            default_args[ClientAttribute.EMAIL.name] = form_email            
        else:
            # email exists.
            pass
        form_username = request.form.get("USERNAME")
        username_exists = ClientModel.query.filter_by(USERNAME = form_username).all() != []
    
        if not username_exists:
            self.UpdateSessionInformation(ClientAttribute.USERNAME, form_username, updateDB=True)
            default_args[ClientAttribute.USERNAME.name] = form_username
        else:
            # username exists already
            pass
        default_args["EMAIL_EXISTS"] = email_exists 
        default_args["USERNAME_EXISTS"] = username_exists

        return default_args
    


    # def CHANGE_PASSWORD_INFORMATION(self, default_args):
    #     old_password = Utility.EncryptSHA256(request.form.get("old-password"))
    #     new_password = request.form.get("new-password")
    #     new_password_confirm = request.form.get("new-password-confirm")

    #     # check if old password entry matches password in db.
    #     if new_password != new_password_confirm:
    #         return "pw not confirmed"

    #     if old_password != self.GetSessionInformation(ClientAttribute.PASSWORD):
    #         return "pw mismatch"
        
    #     if not Utility.IsStrongPassword(new_password):
    #         return "Weak Password"

    #     self.UpdateSessionInformation(ClientAttribute.PASSWORD, new_password, updateDB=True, auto_commit=True)
    #     default_args[ClientAttribute.PASSWORD.name] = new_password
    #     return default_args
    def CHANGE_PASSWORD_INFORMATION(self, default_args):
        old_password = request.form.get("old-password")
        new_password = request.form.get("new-password")
        new_password_confirm = request.form.get("new-password-confirm")
        # check if old password entry matches password in db.
        if new_password != new_password_confirm:
            return "pw mismatch"
        if old_password != new_password_confirm:
            return "pw not confirmed"


        if not Utility.IsStrongPassword(new_password):
            return "Weak Password"

        self.UpdateSessionInformation(ClientAttribute.PASSWORD, Utility.EncryptSHA256(new_password), updateDB=True, auto_commit=True)
        default_args[ClientAttribute.PASSWORD.name] = new_password
        return default_args


    @route("/profile", endpoint="profile",methods=["GET", "POST"])
    def ROUTE_PROFILE(self):
        if not self.IsUserLoggedIn(): return render_template("landingpage.html")
        default_args = {key.name : session[key.name] for key in ClientAttribute}
        # default_args = {"FIRSTNAME" : session["FIRSTNAME"], "LASTNAME" : session["LASTNAME"], "EMAIL": session["EMAIL"], "PASSWORD": session["PASSWORD"], "USERNAME": session["USERNAME"]}
        if request.method == "GET": return render_template("profile.html", **default_args)
        if "submit-profile" in request.form: default_args = self.CHANGE_PROFILE_INFORMATION(default_args)
        elif "submit-password" in request.form: default_args = self.CHANGE_PASSWORD_INFORMATION(default_args)
        try: db.session.commit()
        except Exception as e: print(e)
        return render_template("profile.html", **default_args)

    
    def LOGIN_CONFIRMATION(self, user):
        self.UpdateSessionInformation(ClientAttribute.EMAIL, user.EMAIL)
        self.UpdateSessionInformation(ClientAttribute.USERNAME, user.USERNAME)
        self.UpdateSessionInformation(ClientAttribute.FIRSTNAME, user.FIRSTNAME)
        self.UpdateSessionInformation(ClientAttribute.LASTNAME, user.LASTNAME)
        self.UpdateSessionInformation(ClientAttribute.PASSWORD, user.PASSWORD)
        self.UpdateSessionInformation(ClientAttribute.ACTIVE_SESSION, user.ACTIVE_SESSION)
        self.UpdateSessionInformation(ClientAttribute.ADMIN, user.ADMIN)
        
        self.UpdateSessionInformation(ClientAttribute.PROFILE_PICTURE, user.PROFILE_PICTURE)
        self.UpdateSessionInformation(ClientAttribute.INSTAGRAM_PAGE, user.INSTAGRAM_PAGE)
        self.UpdateSessionInformation(ClientAttribute.FACEBOOK_PAGE, user.FACEBOOK_PAGE)
        self.UpdateSessionInformation(ClientAttribute.LINKEDIN_PAGE, user.LINKEDIN_PAGE)
        self.UpdateSessionInformation(ClientAttribute.TWITTER_PAGE, user.TWITTER_PAGE)
        return redirect("/profile")
        



    # @route("/", endpoint="/")
    # @route("/login/", endpoint="login", methods=['POST', 'GET'])
    # def ROUTE_LOGIN(self):
    #     if request.method == "GET" and not self.IsUserLoggedIn(): return redirect("landingpage")
    #     form_email = request.form.get("email")
    #     form_password = request.form.get("password")
    #     form_fields = [form_email, form_password]
    #     user = self.GetUser({ClientAttribute.EMAIL.name : form_email, ClientAttribute.PASSWORD.name : Utility.EncryptSHA256(form_password)})
    #     if not self.LANDPAGE_VALIDATION_CHECKS(form_fields, user == None):
    #         return render_template("landingpage.html")
    #     return self.LOGIN_CONFIRMATION(user)


    @route("/", endpoint="/")
    @route("/login/", endpoint="login", methods=['POST', 'GET'])
    def ROUTE_LOGIN(self):
        if request.method == "GET" and not self.IsUserLoggedIn(): return redirect("landingpage")
        form_email = request.form.get("email")
        form_password = Utility.EncryptSHA256(request.form.get("password"))
        if not form_email or not form_password: return render_template("login.html")
        user = self.GetUser({ClientAttribute.EMAIL.name : form_email, ClientAttribute.PASSWORD.name : form_password})

        if not self.LOGIN_VALIDATION([form_email, form_password], user == None):
            return render_template("landingpage.html")
        return self.LOGIN_CONFIRMATION(user)

        return self.LOGIN_CONFIRMATION(user)




    # @route("/registration/",endpoint="registration", methods = ["GET", "POST"])
    # def ROUTE_REGISTRATION(self):
        
    #     if self.IsUserLoggedIn() and request.method == "GET": return redirect("/profile")
    #     new_user_details = {
    #         ClientAttribute.EMAIL.name : request.form.get("email"), 
    #         ClientAttribute.USERNAME.name : request.form.get("username"), 
    #         ClientAttribute.FIRSTNAME.name : request.form.get("firstname"), 
    #         ClientAttribute.LASTNAME.name : request.form.get("lastname"), 
    #         ClientAttribute.PASSWORD.name : request.form.get("password"),
    #         ClientAttribute.ACTIVE_SESSION.name : "",
    #         ClientAttribute.ADMIN.name : 0 
    #         }
        
    #     user_exists = self.UserExists(username=new_user_details[ClientAttribute.USERNAME.name], email=new_user_details[ClientAttribute.EMAIL.name])
    #     if self.REGISTERATION_VALIDATION(list(new_user_details.values()), user_exists, new_user_details[ClientAttribute.EMAIL.name], new_user_details[ClientAttribute.PASSWORD.name]):
    #         return redirect("/landingpage") 
        
    #     new_user_details[ClientAttribute.PASSWORD.name] = Utility.EncryptSHA256(new_user_details[ClientAttribute.PASSWORD.name])
    #     user = self.CreateUser(new_user_details)
    #     return self.LOGIN_CONFIRMATION(user)


    @route("/registration/",endpoint="registration", methods = ["GET", "POST"])
    def ROUTE_REGISTRATION(self):
        if self.IsUserLoggedIn() and request.method == "GET": return redirect("/profile")
        new_user_details = {
            ClientAttribute.EMAIL.name : request.form.get("email"), 
            ClientAttribute.USERNAME.name : request.form.get("username"), 
            ClientAttribute.FIRSTNAME.name : request.form.get("firstname"), 
            ClientAttribute.LASTNAME.name : request.form.get("lastname"), 
            ClientAttribute.PASSWORD.name : Utility.EncryptSHA256(request.form.get("password")),
            ClientAttribute.ACTIVE_SESSION.name : "",
            ClientAttribute.ADMIN.name : 0,
            ClientAttribute.PROFILE_PICTURE.name : "",
            ClientAttribute.INSTAGRAM_PAGE.name : "",
            ClientAttribute.FACEBOOK_PAGE.name : "",
            ClientAttribute.TWITTER_PAGE.name : "",
            ClientAttribute.LINKEDIN_PAGE.name : ""

            }
        for key,value in new_user_details.items():
            if value is None:
                return "404"

        if self.UserExists(username=new_user_details[ClientAttribute.USERNAME.name], email=new_user_details[ClientAttribute.EMAIL.name]): redirect("/landingpage")
        user = self.CreateUser(new_user_details)
        return self.LOGIN_CONFIRMATION(user)

    @route("/logout", endpoint="logout")
    def ROUTE_LOGOUT():
        session.clear()
        return redirect("login")

    @route("/session", endpoint="session", methods=["GET", "POST"])
    def ROUTE_MANAGE_SESSIONS(self):
        if request.method == "POST":
            roomID = request.form.get("room")
            matchingRoomClients = ClientModel.query.filter_by(ACTIVE_SESSION = roomID).all()
            
            if "joinsession" in request.form:
                matchingRoomClients = ClientModel.query.filter_by(ACTIVE_SESSION = roomID).all()

                if matchingRoomClients == []:
                    # handle this.
                    return "room id does not exist"
            elif "createsession" in request.form:
                if matchingRoomClients != []:
                    return "session id already exists"

            self.UpdateSessionInformation(ClientAttribute.ACTIVE_SESSION, roomID, updateDB=True)
        return redirect(url_for("chat"))

    @route("/chat", endpoint="chat",methods=["GET"])
    def ROUTE_CHAT_SYSTEM(self):
        if not self.IsUserLoggedIn(): return redirect("landingpage")
        username = self.GetSessionInformation(ClientAttribute.USERNAME)
        active_session = self.GetSessionInformation(ClientAttribute.ACTIVE_SESSION)
        if active_session: return render_template("chat.html", username=username, room=active_session)
        return render_template("session.html")

    @route("/sketchpad", endpoint="sketchpad", methods=["GET", "POST"])
    def ROUTE_SKETCHPAD(self):
        return render_template("sketchpad.html")


    def LOGIN_VALIDATION(self, fields, invalid_existence_status):
        if self.EMPTY_FIELDS_CHECK(fields):
            # Print a message or return an indicator
            return False
        if invalid_existence_status:
            # Print a message or return an indicator
            return False
        return True
    
    def REGISTERATION_VALIDATION(self, fields, invalid_existence_status, email, password):
        if not self.LOGIN_VALIDATION(fields, invalid_existence_status):
            return False
        if not Utility.IsEmailAddress(email):
             # Print a message or return an indicator
            return False
        if not Utility.IsStrongPassword(password):
             # Print a message or return an indicator
            return False
        return True

    def EMPTY_FIELDS_CHECK(self, fields):
        for field in fields:
            if not field:
                return True
        return False


