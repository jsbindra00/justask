import unittest
from app import create_app, connect_db, app_run
import os
import sqlite3


database_name = "test_database.db"
con, cur = connect_db(database_name)
 #data = [['email@gmail.com', 'JS0109', 'John', 'Smith', 'password123', 'Listener']]
         #for i in range(len(data)):
          #   cur.execute("INSERT INTO users VALUES (?,?,?,?, ?, ?)", data[i])

con.commit()

cur.close()
con.close()
os.remove(database_name)