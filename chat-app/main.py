from app import socketio, app, db
from JustAsk import *
from threading import Thread
from Client import ClientModel
from Message import MessageModel





def DebugMode():
    while True:
        arg = input("Enter Server Command").upper()

        if arg == "SAVE_CLIENTS_DB":
            ClientModel.SaveDatabase("./database.txt")
        elif arg == "SAVE_MESSAGES_DB":
            MessageModel.SaveDatabase("./messages.txt")


if __name__ == '__main__':
    Session()
    application = JustAsk()
    from Client import ClientModel
    db.create_all()
    application.Start()

    # debugMode = Thread(target=DebugMode)
    # debugMode.start()
    
    socketio.run(app, debug=False)
    # debugMode.join()


