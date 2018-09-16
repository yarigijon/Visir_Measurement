'''
Copyright (C) 2018  Pablo Baizan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

# coding=utf-8
#import basic_exception
import sys

class ClientRegistry(object):
    def __new__(cls):
        # Implementacion especial del singleton
        if not hasattr(cls, 'instance'): # Si no existe el atributo 'instance'
            cls.instance = super(ClientRegistry, cls).__new__(cls) # lo creamos
        return cls.instance

    def Register(self):
        self.LastClientId = 0
        self.ClientList = []

    def GetClientId(self):
        self.LastClientId += 1
        return self.LastClientId

    def AddClient(self, Client):
        self.ClientList.append(Client)

class Client(object):
    '''Clase que contiene las variables necesarias para definir un cliente'''
    
    def __init__(self):
        '''Constructor que inicializa el objeto cliente''' 
        self.ClientRegistry = ClientRegistry() 
        self.__mpClientID = self.ClientRegistry.GetClientId()
        self.__mpSession = None

    def ConnectionClosed(self):
        '''Cierra el cliente liberando la sesion'''
        if self.__mpSession:
            self.__mpSession.Unlock(self)
        if self.__mpSession and not self.__mpSession.KeepAlive():
            self.__mpSession.Close()
            self.__mpSession = None
    
    def BindToSession(self, pSession):
        '''Asocia la sesion al cliente.
        Parametros:
        pSession -- sesion a asociar'''
        if self.__mpSession and pSession != self.__mpSession:
            self.__mpSession.Unlock(self)
            print "\t\033[31mError:\033[0m Client session has been replaced"
        self.__mpSession = pSession
        return True

    def GetSession(self):
        '''Devuelve la sesion asociada al cliente, además la actualiza, es decir,
        que indica que se esta usando'''
        if self.__mpSession:
            self.__mpSession.Touch()
        return self.__mpSession

    def SessionDestroyed(self):
        '''Recorre el vector de Listeners y destruye las sesiones asociados 
        a estos igualando la sesion a none'''
        if self.__mpSession:
            self.mpSession = None
    
    def ClientId(self):
        '''Retorna el identificador del cliente'''
        return self.__mpClientID