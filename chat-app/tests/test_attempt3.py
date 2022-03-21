import unittest
import requests

class ApiTest(unittest.TestCase):
    HOME_URL = "http://127.0.0.1:5000"
    REGISTER_URL = "http://127.0.0.1:5000/register"
    LOGIN_URL = "http://127.0.0.1:5000/login"
    PROFILE_URL= "http://127.0.0.1:5000/profile"


    def test_regiser_user(test):
        r = requests.get(ApiTest.HOME_URL)
        print(r.url)
        assert r.url == ApiTest.REGISTER_URL

        # payload = dict(email='value1', password='value2')
        # r = requests.post(ApiTest.REGISTER_URL, data=payload)




    # When home page accessed with GET request, if user logged in, 
    # go to profile page, else, go to the login page.
    def test_get_home_page(self):
        r = requests.get(ApiTest.HOME_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.status_code, 200)