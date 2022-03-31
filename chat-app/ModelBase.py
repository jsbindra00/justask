class ModelBase:
    def __init__(self):
        pass


    def ProcessDatabase(clients,filePath):
        f = open(filePath, "w")
        for client in clients:
            f.write(repr(client) + "\n")
        f.close()

    def SaveDatabase(filePath):
        raise NotImplementedError("")