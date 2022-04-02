from SharedContext import socketio, app, db
from JustAsk import *
from threading import Thread
from Client import ClientModel
from Message import MessageModel
from flask_session import Session
import os


def DebugMode():
    while True:
        arg = input("Enter Server Command").upper()

        if arg == "SAVE_CLIENTS_DB":
            ClientModel.SaveDatabase("./database.txt")
        elif arg == "SAVE_MESSAGES_DB":
            MessageModel.SaveDatabase("./messages.txt")

if __name__ == '__main__':

    JustAsk.register(app)

    Session()
    application = JustAsk()
    from Client import ClientModel
    db.create_all()

    # debugMode = Thread(target=DebugMode)
    # debugMode.start()
    
    port = int(os.environ.get('PORT', 5000))
    # debugMode = Thread(target=DebugMode)
    # debugMode.start()

    socketio.run(app, debug=True, host='127.0.0.1', port=port)
    # debugMode.join()


