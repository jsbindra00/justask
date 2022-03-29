from threading import Thread









def SaveDatabase(database):
    thread = Thread(target=__ProcessDatabase, args=(database,))
    thread.start()
    thread.join()





