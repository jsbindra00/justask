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
            print(session[SEARCH_PRED.name])
            current_user = ClientModel.query.filter_by(**{SEARCH_PRED.name : session[SEARCH_PRED.name]}).first()
            setattr(current_user, client_attribute.name, arg)
            if auto_commit: db.session.commit()

    def GetSessionInformation(self, client_attribute):
        return session[ClientAttribute(client_attribute).name]


    def KickUser(self, data):
        
        pass
    
    def IsUserLoggedIn(self):
        return session
    
    def CreateUser(self):
        pass

    def UserExists(self):
        pass

    @route("/signout", endpoint="signout")
    def ROUTE_SIGNOUT(self):
        if self.IsUserLoggedIn():session.clear()
        return redirect("/landingpage")

    @route("/landingpage", endpoint="landingpage")
    @route("/", endpoint="landingpage")
    def ROUTE_LANDING_PAGE(self):
        return redirect("profile") if self.IsUserLoggedIn() else render_template("landingpage.html")

    @route("/leave_session", endpoint="leave_session",methods=["POST"])
    def ROUTE_LEAVE_SESSION(self):
        if session["ACTIVE_SESSION"]: self.UpdateSessionInformation(ClientAttribute.ACTIVE_SESSION, None, updateDB=True)
        return redirect("/profile")
        


    def CHANGE_PROFILE_INFORMATION(self, default_args):

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
    
    def CHANGE_PASSWORD_INFORMATION(self, default_args):
        old_password = Utility.EncryptSHA256(request.form.get("old-password"))
        new_password = Utility.EncryptSHA256(request.form.get("new-password-confirm"))
        # check if old password entry matches password in db.
        if old_password != self.GetSessionInformation(ClientAttribute.PASSWORD):
            return "pw mismatch"
        
        self.UpdateSessionInformation(ClientAttribute.PASSWORD, new_password, updateDB=True, auto_commit=True)
        default_args[ClientAttribute.PASSWORD.name] = new_password
        return default_args

    @route("/profile", endpoint="profile",methods=["GET", "POST"])
    def ROUTE_PROFILE(self):
        if not self.IsUserLoggedIn(): return render_template("landingpage.html")
        default_args = {"FIRSTNAME" : session["FIRSTNAME"], "LASTNAME" : session["LASTNAME"], "EMAIL": session["EMAIL"], "PASSWORD": session["PASSWORD"], "USERNAME": session["USERNAME"]}


        print(default_args)
        if request.method == "GET": return render_template("profile.html", **default_args)
        if "submit-profile" in request.form: default_args = self.CHANGE_PROFILE_INFORMATION(default_args)
        elif "submit-password" in request.form: default_args = self.CHANGE_PASSWORD_INFORMATION(default_args)
        try: db.session.commit()
        except Exception as e:
            print(e)
        return render_template("profile.html", **default_args)

        
    @route("/", endpoint="/")
    @route("/login/", endpoint="login", methods=['POST', 'GET'])
    def ROUTE_LOGIN(self):
        if request.method == "GET":
            if session: return redirect("landingpage")
        form_email = request.form.get("email")
        form_password = Utility.EncryptSHA256(request.form.get("password"))
        if not form_email or not form_password: return render_template("login.html")

        user = ClientModel.query.filter_by(EMAIL=form_email, PASSWORD=form_password).first()
        if  user == None:
            #todo handle this. Invalid login credentials.
            print("INVALID LOGIN CREDENTIALS")
            return render_template("landingpage.html")
        # optimise
        self.UpdateSessionInformation(ClientAttribute.EMAIL, user.EMAIL)
        self.UpdateSessionInformation(ClientAttribute.USERNAME, user.USERNAME)
        self.UpdateSessionInformation(ClientAttribute.FIRSTNAME, user.FIRSTNAME)
        self.UpdateSessionInformation(ClientAttribute.LASTNAME, user.LASTNAME)
        self.UpdateSessionInformation(ClientAttribute.PASSWORD, user.PASSWORD)
        self.UpdateSessionInformation(ClientAttribute.ACTIVE_SESSION, user.ACTIVE_SESSION)
        self.UpdateSessionInformation(ClientAttribute.ADMIN, user.ADMIN)

        return redirect("/profile")

    @route("/registration/",endpoint="registration", methods = ["GET", "POST"])
    def ROUTE_REGISTRATION(self):
        
        if self.IsUserLoggedIn() and request.method == "GET": return redirect("/profile")
        
        
        form_email = request.form.get("email")
        form_username = request.form.get("username")
        form_first_name = request.form.get("firstname")
        form_last_name = request.form.get("lastname")
        form_password = Utility.EncryptSHA256(request.form.get("password"))
        active_session = "0"
        
        data = [form_email, form_username,form_first_name,form_last_name,form_password, active_session]
        for field in data:
            if not field:
                #todo handle this
                return "404"



        user_exists = ClientModel.query.filter_by(EMAIL=form_email).first()
        if user_exists != None :
            #todo handle this. User is already registered, initiate a popup.
            return redirect("/landingpage")

        db.session.add(ClientModel(USERNAME = form_username, FIRSTNAME = form_first_name, LASTNAME = form_last_name, EMAIL = form_email, PASSWORD = form_password, ACTIVE_SESSION = "0", ADMIN = 0))
        db.session.commit()

        return redirect("/profile")

    @route("/chat_logout/", endpoint="chat_logout")
    def chat_logout(self):
        self.UpdateSessionInformation(ClientAttribute.ACTIVE_SESSION, "")
        return redirect("/session")

    @route("/logout", endpoint="logout")
    def logout():
        session.clear()
        return redirect("login")

    @route("/session", endpoint="session", methods=["GET", "POST"])
    def ROUTE_MANAGE_SESSIONS(self):
        if request.method == "GET":
            if self.GetSessionInformation(ClientAttribute.ACTIVE_SESSION) != None:
                return redirect(url_for("chat"))
            return render_template("session.html")
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

    @route("/chat", endpoint="chat")
    def ROUTE_CHAT_SYSTEM(self):
        username = session.get('USERNAME')
        room = session.get('ACTIVE_SESSION')
        if username and room:
            return render_template('chat.html', username=username, room=room)
        else:
            return redirect(url_for('session'))

    @route("/sketchpad", endpoint="sketchpad", methods=["GET", "POST"])
    def ROUTE_SKETCHPAD(self):
        return render_template("sketchpad.html")

