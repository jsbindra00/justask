class ModelBase:
    def __init__(self):
        pass


    def __ProcessDatabase(self, dbitems,filePath):
        raise NotImplementedError("")


    def SaveDatabase(self, filePath):
        raise NotImplementedError("")