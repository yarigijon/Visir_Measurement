#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import sys
# Metodos minimos que deben implementar las clases, por defecto retornan 0
from authentry import IAuthEntry, ICredentials, IAuthenticator
# import syslog
import datetime


# Hereda los metodos minimos de IAuthEntry
class AuthEntry(IAuthEntry):
    '''Objeto que hereda de la clase IAuthEntry'''
    def __init__(self, *arg):
        '''Contructor que inicia el objeto AuthEntry
        Parametros:
        arg-- array con los parametros necesarios para
        inicilizar el objeto'''
        if len(arg) == 0:
            self.__mCookie = ""
            self.__mIP = ""
            # Retorna el maximo valor de un int, esto no es real python
            # tiene tamano dinamico, pero es el equivalente a C,
            # tambien existe sys.maxint pero en python 3 se ha
            # dejado solo este.
            self.__mTimeout = sys.maxsize
            self.__mPrio = 0
        elif len(arg) == 4:
            self.__mCookie = arg[1]
            self.__mIP = arg[2]
            self.__mTimeout = arg[3]
            self.__mPrio = 0
        else:
            self.__mCookie = arg[1]
            self.__mIP = arg[2]
            self.__mTimeout = arg[3]
            self.__mPrio = arg[4]

    def GetCookie(self):
        '''Retorna la cookie asociada al objeto auntentificador'''
        return str(self.__mCookie)

    def GetIP(self):
        '''Retorna la ip asociada al objeto autentificador'''
        return str(self.__mIP)

    def GetTimeout(self):
        '''Retorna el timeout asociado al objeto autentificador'''
        return self.__mTimeout

    def GetPrio(self):
        '''Retorna la prioridad asociada al objeto autentificador'''
        return self.__mPrio

    def SetCookie(self, cookie):
        '''Asocia la cookie al objeto autentificador'''
        self.__mCookie = cookie

    def SetIP(self, ip):
        '''Asocia la IP  al objeto autentificador'''
        self.__mIP = ip

    def SetPrio(self, prio):
        '''Asocia la prioridad al objeto autentificador'''
        self.__mPrio = prio


class Credentials(ICredentials):
    '''Objeto que hereda de Icredentials'''

    def __init__(self, cookie):
        '''Constructor que inicializa las credenciales'''
        self.__mCookie = cookie

    def GetCookie(self):
        '''Retorna la cookie asociada al objeto credenciales'''
        return str(self.__mCookie)


class Authentication(object):
    '''Clase que define el objeto autentificacion'''

    def __new__(cls):
        # Implementacion especial del singleton
        # Si no existe el atributo 'instance', lo creamos
        if not hasattr(cls, 'instance'):
            cls.instance = super(Authentication, cls).__new__(cls)
        return cls.instance

    def Register(self, pSessionReg, allowKeepAlive, bypassAuth):
        '''Constructor que inicializa la clase autentificacion.
           Parametros:
           pSessionReg -- Objeto sesion registry donde se almacenan
                          las sesiones
           allowKeepAlive -- Indica si la sesion tiene que seguir
                             abierta o no
           bypassAuth-- Indica si es necesario hacer autentificacion o no'''
        self.__mBypassAuth = bypassAuth
        self.__mAllowKeepAlive = allowKeepAlive
        self.__mpSessionReg = pSessionReg
        self.__mCacheId = 1
        self.__mAuthenticators = []

    def __del__(self):
        '''Destructor, si queda algun metodo de auntentificacion
        indica un aviso.'''
        if len(self.__mAuthenticators) > 0:
            # modificar por syserr de syslog.py
            print("Warning: One or more authentication modules"
                  " was not unregistered", sys.stderr)

    def RegisterAuthenticator(self, pAuth):
        ''' Registra el metodo autentificador
        Parametros:
        pAuth-- IAuthenticator a añadir en el array de autentificadores'''
        self.__mAuthenticators.append(pAuth)
        return 1

    def UnregisterAuthenticator(self, pAuth):
        ''' Desregistra el metodo autentificador
        Parametros:
        pAuth-- IAuthenticator a borrar en el array de autentificadores'''
        self.__mAuthenticators.remove(pAuth)
        return 1

    def Init(self):
        '''Iniciliza los autentificadores, en el caso de ser posible'''
        if self.__mBypassAuth:
            return True
        for it in self.__mAuthenticators:
            # chequeamos que existe el metodo init y se puede llamar
            if not (hasattr(it, "Init") and callable(getattr(it, "Init"))):
                print("Failed to Init authenticator", sys.stderr)
                return False
            # intentamos inicializar si no inicializa error
            if not it.Init():
                print("Failed to Init authenticator", sys.stderr)
                return False
        return True

    def Tick(self):
        '''Aumenta el identificador de cache'''
        self.__mCacheId += 1
        return True

    def Authenticate(self, pClient, cookie, keepalive):
        '''Metodo que dado un cliente, y la cookie lo autentifica
           si es posible
           Parametros:
                pClient -- Cliente a autentificar
                cookie -- cookie
                keepalive -- Booleano que indica si permite el
                            keepalive o no'''
        if keepalive and not self.__mAllowKeepAlive:
            Now = str(datetime.datetime.now())
            print ("[" + Now + "] \033[31mError:\033[0m Client is trying"
                   " to use keepalive when it is not allowed")
            return False, None
        if self.__mBypassAuth:
            entry = AuthEntry(cookie, "<unknown>", 0xffffffff, 5)
            return self.CreateSession(pClient, cookie, keepalive, entry)
        # Chequeamos si hay una sesion utilizando la cookie
        pSession = self.__mpSessionReg.GetSessionFromCookie(cookie)
        if pSession:
            # si la cookie esta en uso chequeamos que ha sido
            # bloqueada por este cliente
            if not pSession.Lock(pClient):
                stream = ("[" + str(datetime.datetime.now()) + "] " +
                          "Cookie already in use by other client")
                return False, None
            stream = ("[" + str(datetime.datetime.now()) +
                      "] " + "Session re-bound to new client")
            print(stream)
            pClient.BindToSession(pSession)
            return True, None
        aCred = Credentials(cookie)
        aAuthEntry = AuthEntry()
        for it in self.__mAuthenticators:
            if it.FetchAuthEntry(aCred, aAuthEntry, self.__mCacheId):
                return self.CreateSession(
                            pClient, cookie, keepalive, aAuthEntry)
        return False, None

    def CreateSession(self, pClient, cookie, keepalive, pEntry):
        ''' Crea la sesion asociada a un cliente cuando este se autentifica
        Parametros:
        pClient--Cliente al que se asigna la sesion
        cookie-- cookie para la creacion de la sesion
        keepalive-- booleano que indica si la sesion se crea con keepalive o no
        pEntry-- IAuthEntry que identifica al autentificador'''
        # XXX:es necesario manejar el caso fallido
        pSession = self.__mpSessionReg.CreateSession(cookie, keepalive, pEntry)
        if pSession:
            if not pSession.Lock(pClient):
                return False, None
            return True, pSession
        else:
            return False, None
