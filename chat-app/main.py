from app import socketio, app, clientsDB
from JustAsk import *
from threading import Thread
from Client import ClientModel





def DebugMode():
    while True:
        arg = input().upper()

        if arg == "SAVE_CLIENTS_DB":
            ClientModel.SaveDatabase("./database.txt")
            continue


if __name__ == '__main__':
    Session()
    application = JustAsk()
    from Client import ClientModel
    clientsDB.create_all()
    application.Start()
    debugMode = Thread(target=DebugMode)
    debugMode.start()
    socketio.run(app, debug=True)
    debugMode.join()


