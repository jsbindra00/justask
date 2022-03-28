from app import socketio, app, clientsDB
from JustAsk import *

if __name__ == '__main__':
    Session()
    application = JustAsk()
    from Client import ClientModel
    clientsDB.create_all()
    application.Start()
    socketio.run(app, debug=True)


