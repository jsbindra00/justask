import unittest
from app import create_app, connect_db, app_run
import os
import sqlite3




class MyTestCase(unittest.TestCase):
    API_URL = "127.0.0.1:5000/"
    database_name = "justaskdatabase.db"
    """
    def test_DatabaseCreation(self):
        database_name = "justaskdatabase.db"
        if os.path.exists(database_name):
            os.remove(database_name)
        self.assertEqual(os.path.exists(database_name), False)
        connect_db()
        self.assertEqual(os.path.exists(database_name), True)

    def test_DatabaseCorrectness(self):
        table_information = [["users", "email", "username", "first_name", "last_name", "password", "role"],
                             ["messages", "email", "message", "username", "first_name", "last_name", "role"]]
        con, cur = connect_db()
        columns = []
        for i in range(2):
            listOfTables = cur.execute(
                "SELECT tableName FROM sqlite_master WHERE type='table' AND name=" + table_information[i][0] + ";").fetchall()
            self.assertNotEqual(listOfTables, [])
            columns.append(i[1] for i in cur.execute('PRAGMA table_info(main)'))
        for i in range(2):
            for j in range(1, 7):
                self.assertEqual(columns[i][j], table_information[i][j])

    def testDatabaseConnection(self):
        
        database_name = "justaskdatabase.db"
        self.test_DatabaseCreation()
        os.rename(database_name, "database_test_rename.db")
        self.assertEqual(os.path.exists(database_name), False)
        con, cur = connect_db()
        # terminate_ test that nothing exists
        self.assertEqual(os.path.exists(database_name), True)
        os.remove(database_name)
        os.rename("database_test_rename.db", database_name)
        con, cur = connect_db()
        # terminate_ test if expected values exists

    def createDatabase(self):
        self.testDatabaseCreation()
        con, cur = connect_db()
        data = [""]
        for i in range(len(data)):
            cur.execute("INSERT INTO users VALUES (?,?,?,?, ?, ?)", data[i])
        # Save (commit) the changes
        con.commit()"""

    def test_something(self):
        database_name = "test_database.db"
        con, cur = connect_db(database_name)
        #data = [['email@gmail.com', 'JS0109', 'John', 'Smith', 'password123', 'Listener']]
        #for i in range(len(data)):
         #   cur.execute("INSERT INTO users VALUES (?,?,?,?, ?, ?)", data[i])

        con.commit()

        cur.close()
        con.close()
        os.remove(database_name)

if __name__ == '__main__':
    unittest.main()
