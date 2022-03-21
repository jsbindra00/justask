import sqlite3

connect = sqlite3.connect('justaskdatabase.db')

cursor = connect.cursor()

existTable = cursor.execute("""
    SELECT tableName 
    FROM sqlite_master 
    WHERE type='table'
    AND tableName='justasktable'; 
    """).fetchall()

if existTable == []:
    cursor.execute("""
    CREATE TABLE justasktable (
        id INTEGER PRIMARY KEY,
        first_name DATATYPE,
        last_name DATATYPE,
        username DATATYPE,
        email DATATYPE,
        password DATATYPE);
    """)

cursor.execute("""
    INSERT INTO justasktable VALUES ();
    """)

cursor.execute("""
    SELECT * FROM justasktable WHERE stuff;
    """)

connect.commit()

connect.close()