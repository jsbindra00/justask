import unittest
import requests
import sqlite3
import os
from app_3 import JustAsk

class ApiTest(unittest.TestCase):

    def setUp(self):
        # URLs
        self.HOME_URL = "/"
        self.REGISTER_URL = "/registration"
        self.LOGIN_URL = "/login"
        self.PROFILE_URL= "/profile"

        #setup application
        self.db = "test_justaskdatabase.db" 
        self.application = JustAsk()
        self.application.create_app(self.db)
        self.application.app.testing = True
        self.client = self.application.app.test_client()

        # setup db


    # remove the setup data from db
    def tearDown(self):
        pass
        # self.application.cursor.close()
        # self.application.connection.close()
        # os.remove(self.db)
    
    # test getting all routes works
    def test_get(self):
        response = self.client.get(self.HOME_URL)
        assert response.status_code == 200

        response = self.client.get(self.REGISTER_URL)
        assert response.status_code == 200

        # Talk to jas about sessions to sort this out. The problem is the redirection to login when accessing the profile url.
        response = self.client.get(self.PROFILE_URL)
        assert response.status_code == 200 

        # ...

    
    def test_register_user_with_correct_details(self):
        # email should start of not being in db
        test_data = dict(email='JohnSmith12@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password = 'password1234')
        email_present = self.application.search_data("SELECT * FROM users WHERE email= ?", (test_data["email"],))
        assert email_present == []
        
        # after post, user should be redirected, and data should be present in db
        r = self.client.post(self.REGISTER_URL, data= test_data)
        email_present = self.application.search_data("SELECT * FROM users WHERE email= ?",(test_data["email"],))
        assert email_present != []
        assert r.url == self.LOGIN_URL

    # Ideas
    # assert b"<h2>Hello, World!</h2>" in response.data
    #     response = client.post("/user/2/edit", data={
    #     "name": "Flask",
    #     "theme": "dark",
    #     "picture": (resources / "picture.png").open("rb"),
    # })
    # assert response.status_code == 200


    
if __name__ == "__main__":
    unittest.main()
    