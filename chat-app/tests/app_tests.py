import email
import unittest
import requests
import sqlite3
import os
from app import connect_db

class ApiTest(unittest.TestCase):
<<<<<<<< HEAD:chat-app/tests/app_tests.py
    
    HOME_URL = "http://127.0.0.1:5000"
    REGISTER_URL = "http://127.0.0.1:5000/register"
    LOGIN_URL = "http://127.0.0.1:5000/login"
    PROFILE_URL= "http://127.0.0.1:5000/profile"

    DATABASE_NAME = "justaskdatabase.db"
    TEST_DATABASE_NAME = "test_" + DATABASE_NAME

    connect = None
    cursor = None
    SETUP_DATA = [['email@gmail.com', 'JS0109', 'John', 'Smith', 'password123', 'Listener']]

    # test data:
    same_email = dict(email='email@gmail.com', first_name='value2', last_name = 'v', username = 'a', password = 'a', role = 'Speaker')
========

    def __init__(self):
        self.HOME_URL = "http://127.0.0.1:5000"
        self.REGISTER_URL = "http://127.0.0.1:5000/register"
        self.LOGIN_URL = "http://127.0.0.1:5000/login"
        self.PROFILE_URL= "http://127.0.0.1:5000/profile"

        self.DATABASE_NAME = "justaskdatabase.db"
        self.TEST_DATABASE_NAME = "test_" + self.DATABASE_NAME

        self.connect = None
        self.cursor = None
        self.SETUP_DATA = [['email@gmail.com', 'JS0109', 'John', 'Smith', 'password123', 'Listener']]

        # test data:
        self.same_email = dict(email='email@gmail.com', first_name='value2', last_name = 'v', username = 'a', password = 'a', role = 'Speaker')
>>>>>>>> mcq:chat-app-backup/test/api_test_app_test
    
    
    # setup db with the setup data
    def setUp(self):
        self.connect, self.cursor = connect_db(self.TEST_DATABASE_NAME)
        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", self.SETUP_DATA[0])
        self.connect.commit()

    # remove the setup data from db
    def tearDown(self):
        self.cursor.close()
        self.connect.close()
        os.remove(self.TEST_DATABASE_NAME)


    def test_register_user_with_correct_details(self):
        # email should start of not being in db
        test_data = dict(email='value3', first_name='value2', last_name = 'v', username = 'a', password = 'a', role = 'Speaker')
        email_present = self.cursor.execute("SELECT * FROM users WHERE email= ?",(test_data["email"],)).fetchall()
        assert email_present == []
        
        # after post, user should be redirected, and data should be present in db
        r = requests.post(self.REGISTER_URL, data= test_data)
        email_present = self.cursor.execute("SELECT * FROM users WHERE email= ?",(test_data["email"],)).fetchall()
        assert r.url == ApiTest.LOGIN_URL
        assert email_present != []


    def test_access_home_page_unsigned_in(self):
        r = requests.get(ApiTest.HOME_URL)
        assert r.url == ApiTest.LOGIN_URL


    @unittest.skip
    def test_access_home_page_signed_in(self):
        r = requests.get(ApiTest.HOME_URL)
        assert r.url == ApiTest.PROFILE_URL

    # When home page accessed with GET request, if user logged in, 
    # go to profile page, else, go to the login page.
    def test_get_home_page(self):
        r = requests.get(ApiTest.HOME_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.status_code, 200)
    
    def test_database_creation(self):
        self.connect, self.cursor = connect_db(self.TEST_DATABASE_NAME)
        self.cursor.close()
        self.connect.close()
        self.assertEqual(os.path.exists(self.TEST_DATABASE_NAME), True)
        os.remove(self.TEST_DATABASE_NAME)
        self.assertEqual(os.path.exists(self.TEST_DATABASE_NAME), False)
        self.connect, self.cursor = connect_db(self.TEST_DATABASE_NAME)
        self.cursor.close()
        self.connect.close()
        self.assertEqual(os.path.exists(self.TEST_DATABASE_NAME), True)

    def test_get_data_from_login():
        pass

    def test_empty_feilds_handle_login():
        pass

    def test_login_validation():
        pass

    def test_data_stored_in_session():
        pass

    def test_get_data_from_register():
        pass

    def test_validate_register_details():
        pass

    def test_empty_feilds_handle_register():
        pass

    def test_register_then_login():
<<<<<<<< HEAD:chat-app/tests/app_tests.py
        pass
========
        pass

    def test_chat_login():
        pass
    
    def test_chat_room():
        pass

    def test_sending_messages():
        pass
    
    def test_join_room_event():
        pass
    
    def test_leave_room_event():
        pass

if __name__ == "__main__":
    unittest.main()
>>>>>>>> mcq:chat-app-backup/test/api_test_app_test