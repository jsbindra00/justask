import unittest
import requests
import sqlite3
import os
from app import connect_db, insert_data, search_data


# These tests all work for now. We just need to understand how to start a new app with a specific db file.

class ApiTest(unittest.TestCase):

    def setUp(self):
        self.HOME_URL = "http://127.0.0.1:5000/"
        self.REGISTER_URL = "http://127.0.0.1:5000/registration/"
        self.LOGIN_URL = "http://127.0.0.1:5000/login/"
        self.PROFILE_URL= "http://127.0.0.1:5000/profile/"

        # self.DATABASE_NAME = "justaskdatabase.db"
        # self.TEST_DATABASE_NAME = "test_" + self.DATABASE_NAME

        # self.SETUP_DATA = [['email@gmail.com', 'JS0109', 'John', 'Smith', 'password123', "0"]]

        # # test data:
        # self.same_email = dict(email='duplicate@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password = 'password1234')4

        # self.connect, self.cursor = connect_db(self.TEST_DATABASE_NAME)
        # self.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", self.SETUP_DATA[0])
        # self.connect.commit()




    # positive tests:
    def test_register_user_with_correct_details(self):
        # email should start of not being in db
        test_data = dict(email='JohnSmith123@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password = 'password1234')
        email_present = search_data("SELECT * FROM users WHERE email= ?", (test_data["email"],))
        assert email_present == []
        
        # after post, user should be redirected, and data should be present in db
        r = requests.post(self.REGISTER_URL, data= test_data)
        email_present = search_data("SELECT * FROM users WHERE email= ?",(test_data["email"],))[0]
        assert test_data["email"] in email_present
        assert r.url == self.LOGIN_URL


    def test_access_home_page_unsigned_in(self):
        r = requests.get(self.LOGIN_URL)
        assert r.url == self.LOGIN_URL


    def test_access_home_page_signed_in(self):
        r = requests.get(self.HOME_URL)
        assert r.url == self.HOME_URL        







    # Negative tests:
    def test_register_user_with_duplicate_email(self):
        # Right now i am assuming this data has been placed in the db beforehand. We will probably want to do this in the setup when we figure out how to run and app with a specific db file
        test_data = dict(email='duplicate@gmail.com', firstname='John', lastname = 'Smith', username = 'John12', password = 'password1234')
        email_present = search_data("SELECT * FROM users WHERE email= ?", (test_data["email"],))[0]
        assert test_data["email"] in email_present

        # after post, user should be returned to registration page as the email is already stored in the db, and their registration failed
        r = requests.post(self.REGISTER_URL, data= test_data)
        email_present = search_data("SELECT * FROM users WHERE email= ?",(test_data["email"],))
        assert len(email_present) == 1   # only one row is found (the row already stored before the post)
        assert r.url == self.REGISTER_URL





    # # When home page accessed with GET request, if user logged in, 
    # # go to profile page, else, go to the login page.
    def test_get_home_page(self):
        r = requests.get(self.HOME_URL)
        self.assertEqual(r.status_code, 200)
    
    def test_database_creation(self):
        self.cursor.close()
        self.connect.close()
        self.assertEqual(os.path.exists(self.TEST_DATABASE_NAME), True)
        os.remove(self.TEST_DATABASE_NAME)
        self.assertEqual(os.path.exists(self.TEST_DATABASE_NAME), False)
        self.connect, self.cursor = connect_db(self.TEST_DATABASE_NAME)
        self.assertEqual(os.path.exists(self.TEST_DATABASE_NAME), True)

    def test_start_app(self):
        r = requests.get(self.HOME_URL)
        self.assertEqual(r.status_code, 200)
    
    def test_render_landpage(self):
        pass

    def test_get_data_from_login(self):
        pass

    def test_empty_feilds_handle_login(self):
        pass

    def test_login_validation(self):
        pass

    def test_data_stored_in_session(self):
        pass

    def test_get_data_from_register(self):
        pass

    def test_validate_register_details(self):
        pass

    def test_empty_feilds_handle_register(self):
        pass

    def test_register_then_login(self):
        pass

    def test_chat_login(self):
        pass
    
    def test_chat_room(self):
        pass

    def test_sending_messages(self):
        pass
    
    def test_join_room_event(self):
        pass
    
    def test_leave_room_event(self):
        pass

    # remove the setup data from db
    def tearDown(self):
        pass
        # self.cursor.close()
        # self.connect.close()
        # os.remove(self.TEST_DATABASE_NAME)
    
if __name__ == "__main__":
    unittest.main()