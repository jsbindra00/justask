from turtle import end_poly
from flask import Flask, redirect, render_template, request
from flask_classful import FlaskView, route
from random import choice
# we'll make a list to hold some quotes for our app
app = Flask(__name__)
class JustAsk(FlaskView):
    route_base = "/"
    
    # @route("/")
    # @route("/login", endpoint="login")
    # def login(self):

    #     if request.method == "GET":
    #         return render_template("login.html")

    #     # Get user login details
    #     email = request.form.get("email")
    #     password = request.form.get("password")

    #     # Validate submission
    #     login_details = [email, password]
    #     for field in login_details:
    #         if not field:
    #             #todo handle this
    #             return render_template("login.html")


    @route("/", endpoint="/")
    @route("/login/", endpoint="login")
    def login(self):
        # return render_template("login.html")
        if request.method == "GET":
            return render_template("login.html")

        # Get user login details
        email = request.form.get("email")
        password = request.form.get("password")

        # return render_template("login.html")

        # Validate submission
        login_details = [email, password]
        for field in login_details:
            if not field:
                #todo handle this
                return render_template("login.html")

        # If the user provided details stored in the database, add these details to the session, 
        # and send them to their profile page


        # user = self.cursor.execute("SELECT * FROM users WHERE email= ? AND password = ?",(email, password)).fetchone()
        # print("USER " + user)
        # if  user == None:  

        #     print("USER IS NONE")
        #     #todo handle this. Invalid login credentials.
        #     return render_template("login.html")

        # session["email"] = user[0]
        # session["username"] = user[1]
        # session["first_name"] = user[2]
        # session["last_name"] = user[2]
        # session["role"] = user[4]

        return redirect("/profile")

    @route("/registration", endpoint="registration")
    def registration(self):
        return render_template("registration.html")



   

JustAsk.register(app)

if __name__ == '__main__':

    print("helloooo")
    app.run(debug=True)