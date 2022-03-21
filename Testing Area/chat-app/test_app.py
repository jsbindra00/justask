import unittest
import requests
from app import create_app, connect_db, app_run
import os
import sqlite3
import pytest




class MyTestCase(unittest.TestCase):

    def test_request_example(client):
        response = client.get("/posts")
        assert b"<h2>Hello, World!</h2>" in response.data


    def test_something(self):
        database_name = "test_database.db"
        con, cur = connect_db(database_name)
        data = [['email@gmail.com', 'JS0109', 'John', 'Smith', 'password123', 'Listener']]
        for i in range(len(data)):
           cur.execute("INSERT INTO users VALUES (?,?,?,?, ?, ?)", data[i])

        con.commit()

        cur.close()
        con.close()
        os.remove(database_name)

if __name__ == '__main__':
    unittest.main()
