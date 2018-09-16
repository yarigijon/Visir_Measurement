class MaxFilesRegistry (object):

    def __new__(cls):
        # Implementacion especial del singleton
        if not hasattr(cls, 'instance'): # Si no existe el atributo 'instance'
            cls.instance = super(MaxFilesRegistry, cls).__new__(cls) # lo creamos
        return cls.instance

    def Register (self):
        self.Maxfiles = []

    def AddMaxFile(self, MaxFile):
        self.Maxfiles.append(MaxFile)

    def GetMaxFiles(self):
        return self.Maxfiles