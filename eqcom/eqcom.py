'''
Copyright (C) 2018  Pablo Baizan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

from socket import *
import datetime
import threading
import time


def ProcessRequests():
    EQServer = EQCom()
    while(EQServer.Run):
        if EQServer.Requests:
            EQServer.Connect()  # Connect
            Pair = EQServer.Requests.pop(0)
            EQServer.EQServer.send(Pair[1])
            Response = EQServer.EQServer.recv(10000)  # Get response
            EQServer.Responses.append((Pair[0], Response))
            EQServer.Close()


class EQCom(object):

    def __new__(cls):
        # Implementacion especial del singleton
        # Si no existe el atributo 'instance', lo creamos
        if not hasattr(cls, 'instance'):
            cls.instance = super(EQCom, cls).__new__(cls)
        return cls.instance

    def Connect(self):
        self.EQServer = socket(AF_INET, SOCK_STREAM)
        self.EQServer.connect((self.EQServerIP, self.Port))

    def Close(self):
        self.EQServer.close()

    def Register(self, EQServerIP, Port):
        self.EQServer = socket(AF_INET, SOCK_STREAM)
        self.EQServerIP = EQServerIP
        self.Port = Port
        self.Requests = []
        self.Responses = []
        self.Run = True
        EQComThrear = threading.Thread(target=ProcessRequests, name='EQCom')
        EQComThrear.start()
        Now = str(datetime.datetime.now())
        print "[" + Now + "] Registering EQCOM Module"

    def Unregister(self):
        self.Run = False

    def GetResponse(self, KeySession):
        # Todo: Anadir timeout
        Found = False
        while not Found:
            for i in range(0, len(self.Responses)):
                Pair = self.Responses[i]
                if Pair[0] == KeySession:
                    Found = True
                    Response = Pair[1]
                    self.Responses.remove(Pair)
        return Response

    def SendComand(self, SessionKey, Comand):
        Pair = (SessionKey, Comand)
        self.Requests.append(Pair)
