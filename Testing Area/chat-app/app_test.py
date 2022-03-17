# Basic template testing class i am testing

import unittest
import os
import sys
import sqlite3

class DatabaseTestCase(unittest.TestCase):

    def testDatabaseCreation(self):
        database_name = "justaskdatabase.db"
        app_name = "app.py"
        if os.path.exists(database_name):
            os.remove(database_name)
        self.assertEqual(os.path.exists(database_name), False)
        os.system(app_name)
        self.assertEqual(os.path.exists(database_name), True)

    def testDatabaseCorrectness(self, database_name):
        table_information = [["users", "email", "username", "first_name", "last_name", "password", "role"],
                             ["messages", "email", "message", "username", "first_name", "last_name", "role"]]
        con = sqlite3.connect(database_name)
        cur = con.cursor()
        columns = []
        for i in range(2):
            listOfTables = cur.execute(
                """SELECT tableName FROM sqlite_master WHERE type='table'
                AND name=table_information[i][0]; """).fetchall()
            self.assertNotEqual(listOfTables, [])
            columns.append(i[1] for i in cur.execute('PRAGMA table_info(main)'))
        for i in range(2):
            for j in range(1, 7):
                self.assertEqual(columns[i][j], table_information[i][j])

    def testDatabaseConnection(self, database_name, app_name):
        self.createDatabase(database_name)
        os.rename(database_name, "database_test_rename.db")
        self.assertEqual(os.path.exists(database_name), False)
        os.system(app_name)
        # terminate_ test that nothing exists
        self.assertEqual(os.path.exists(database_name), True)
        os.remove(database_name)
        os.rename("database_test_rename.db", database_name)
        os.system(app_name)
        # terminate_ test if expected values exists

    def createDatabase(self, database_name):
        self.testDatabaseCreation()
        connect = sqlite3.connect(database_name)
        cursor = connect.cursor()
        data = [""]
        for i in range(len(data)):
            cursor.execute("INSERT INTO users VALUES (?,?,?,?, ?, ?)", data[i])
        # Save (commit) the changes
        connect.commit()

if __name__ == '__main__':
    unittest.main()