import unittest
import requests
from app import create_app, connect_db, app_run
import os
import sqlite3
import pytest

@pytest.fixture()
def app():
    app, socketio = create_app()
    app.config.update({
        "TESTING": True,
    })


    yield app

    # clean up / reset resources here

@pytest.fixture()
def setup_db():
    database_name = "test_database.db"
    con, cur = connect_db(database_name)
    data = [['email@gmail.com', 'JS0109', 'John', 'Smith', 'password123', 'Listener']]
    for i in range(len(data)):
        cur.execute("INSERT INTO users VALUES (?,?,?,?, ?, ?)", data[i])

    con.commit()

    yield app

    cur.close()
    con.close()
    #os.remove(database_name)

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()