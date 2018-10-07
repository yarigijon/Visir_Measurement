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
# sys.path.append("C:\\Users\\Susana\\Documents\\GitHub\\visir\\Software")
# from instruments.instrumentblock import InstrumentBlock
from circuitsolver.basic_exception import BasicException
from datetime import datetime
import time
import hashlib
import random


class Session(object):
    '''Objeto Sesion que contiene los elementos necesario
       para definir una sesion.'''
    sSessionCounter = 1
    __mpTransaction = None

    def __init__(self, pSessionReg, key, cookie, keepalive, prio):
        '''Constructor que inicializa todas las variables necesarias
        para definir una sesion.'''
        self.__mpSessionReg = pSessionReg
        self.sSessionCounter += 1
        self.__mNumber = self.sSessionCounter
        self.__mKey = key
        self.__mCookie = cookie
        self.__mKeepAlive = keepalive
        self.__mPrio = prio
        self.__mCreatedAt = time.time()
        self.__mValidUntil = -1
        self.__mLastActive = time.time()
        self.__mpLock = False

    def GetNumber(self):
        '''Retorna el numero de sesion'''
        return self.__mNumber

    def GetKey(self):
        '''Retorna la clave de la sesion'''
        return self.__mKey

    def GetBlock(self):
        '''Retorna el objeto instrument block asociado a la sesion'''
        return self.__mpBlock

    def GetCreatedAt(self):
        '''Retorna la fecha de creacion de la sesion'''
        return self.__mCreatedAt

    def GetCookie(self):
        '''Retorna la cookie asociada a la sesion'''
        return self.__mCookie

    def KeepAlive(self):
        '''Retorna si la sesion debe seguri viva a no'''
        return self.__mKeepAlive

    def LastActive(self):
        ''''Retorna la ultima vez que la sesion ha estado activa'''
        return self.__mLastActive

    def GetLock(self):
        '''Retorna si la sesion esta bloqueada o no'''
        return self.__mpLock

    def GetPriority(self):
        '''Retorna la prioridad de la sesion'''
        return self.__mPrio

    def Close(self):
        '''Cierra la sesion'''
        self.__mpSessionReg.CloseSession(self)

    def Touch(self):
        '''Actualiza la variable que indica cuando fue utilizada la sesion
           por ultima vez, actualizando el tiempo de esta con
           la fecha-hora actual'''
        self.__mLastActive = time.time()

    def Lock(self, pClient):
        ''''Bloquea una sesion con respecto a un cliente, comprobando previamente
        que no esta bloquedada y que esa sesion pertence a ese cliente'''
        if self.__mpLock and (pClient != self.__mpLock):
            return False
        if not pClient.BindToSession(self):
            return False
        self.__mpLock = pClient
        return True

    def Unlock(self, pClient):
        '''Desbloquea la sesion de un cliente'''
        if self.__mpLock != pClient:
            return False
        self.__mpLock = None
        return True

    def LessPrioThan(self, pOther):
        '''Comprueba la prioridad de una sesion con respecto a otra pasada
        como parametro, si las prioridades son iguales, la que se haya creado
        primero tiene mayor prioridad'''
        if self.__mPrio < pOther.GetPrio():
            return True
        if self.__mCreatedAt > pOther.GetCreatedAt():
            return True
        return False

    def SetActiveTransaction(self, pTransaction):
        '''Se asocia una transacion pasada como parametro a la sesion'''
        if self.__mpTransaction and pTransaction is not None:
            raise BasicException("Transaction already in progress")
        self.__mpTransaction = pTransaction

    def HasActiveTransaction(self):
        '''Retorna verdadero si hay una transaccion activa,
           o falso en otro caso'''
        return (self.__mpTransaction != 0)


class SessionRegistry(object):
    '''Objeto sesion registry que maneja las sesiones.'''

    def __new__(cls):
        # Implementacion especial del singleton
        # Si no existe el atributo 'instance', lo creamos
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionRegistry, cls).__new__(cls)
        return cls.instance

    def Register(self, maxSessions, sessionTimeout):
        '''Inicializa la calse SessionRegistry.
        Parametros:
        maxSession -- numero de maximo de sesiones permitidas
        sessionTimeout -- periodo de tiempo que una sesion puede
        estar inactiva'''
        self.__mMaxSessions = maxSessions
        self.__mSessionTimeout = sessionTimeout
        self.__mSessions = {}

    def __del__(self):
        '''Borrar el array de sesiones'''
        for key, value in self.__mSessions.items():
            del self.__mSessions[key]

    def CreateSession(self, cookie, keepalive, entry):
        '''Crea la sesion.
        Parametros:
        cookie -- cookie a asociar con la sesion
        keepalive -- indica si se debe manterer vivo durante
                    un periodo de tiempo
        entry -- parametros de inteficacion de la autenficacion
                 (cookie, ip, prioridad)'''
        if entry:
            prio = entry.GetPrio()
        else:
            prio = 0
        if len(self.__mSessions) >= self.__mMaxSessions:
            # buscamos y destruimos una sesion con menor prioridad que esta
            # si no existe no podemos crear sesion
            if not self.DestroyLeastPrio(prio):
                return None
        sessionkey = self.GenerateName()
        pNewSession = Session(self, sessionkey, cookie, keepalive, prio)
        self.__mSessions[sessionkey] = pNewSession
        return pNewSession

    def CloseSession(self, pSession):
        '''Destruye la sesion pasada como parametro, en el caso de existir.
        Parametros:
        pSession-- Sesion a cerrar.'''
        for key, value in self.__mSessions.items():
            if value == pSession:
                self.DestroySession(pSession)
                del self.__mSessions[key]
                return

    def GetSession(self, sessionkey):
        '''Obtiene la sesion a partir del identificador de sesion.
        Parametros:
        sessionkey -- Id de sesion'''
        finder = self.__mSessions.get(sessionkey)
        if finder:
            return finder
        return 0

    # TODO: eliminar esta funcion no se usa además de tener parametros de más
    def CheckCookie(self, pClient, cookie):
        ''''Comprueba que si una cookie esta libre o es usada por una sesion'''
        for key, value in self.__mSessions.items():
            if value.GetCookie() == cookie:
                return False
        return True

    def GetSessionFromCookie(self, cookie):
        '''Retorna la sesion asociada a una determinada cookie.
        Parametros:
        cookie -- cookie a buscar asociada a una sesion'''
        for key, value in self.__mSessions.items():
            if value.GetCookie() == cookie:
                return value
        return None

    def Tick(self):
        '''Comprueba si las sesiones siguen activas, es decir, han sido
        usadas detro de un periodo de tiempo, y sino las destruye'''
        timeout = self.__mSessionTimeout
        now = time.time()
        for key, value in self.__mSessions.items():
            if value.LastActive() < (now - timeout):
                stream = ("[" + str(datetime.now()) + "] " +
                          "Session timed out: " + value.GetNumber())
                print(stream)
                self.DestroySession(value)
                del self.__mSessions[key]
        return True

    def GenerateName(self):
        '''Genera el identificador de la sesion'''
        input = "visir session hash seed"
        # input = "openlabs session hash seed" # original
        input += str(time.time())
        input += str(random.randint(0, 32767))
        input += str(Session.sSessionCounter)
        md5sum = hashlib.md5()
        md5sum.update(input)
        output = str(md5sum.hexdigest())
        return output

    def DestroySession(self, pSession):
        '''Destruye la sesion que se pasa como parametro.
        Parametros:
        pSession -- Sesion a destruir'''
        # we better make sure this lock is updated, or this will crash horribly
        if pSession.GetLock():
            pSession.GetLock().SessionDestroyed()
        del pSession

    def DestroyLeastPrio(self, lowerthan):
        '''Este metodo destuye aquellas sesion que tiene menor prioridad
           que la prioridad indicada como parametros.
           Parametros:
               lowerthan -- Entero que indica la prioridad por debajo de
                            la cual todas las sesiones seran destruidas '''
        currentit = None
        for key, value in self.__mSessions.items():
            if value.GetPriority() < lowerthan:
                if currentit is not None:
                    if currentit.LastActive() > value.LastActive():
                        currentit = value
                        currentkey = key
                else:
                    currentit = value
                    currentkey = key
        if currentit:
            stream = ("[" + str(datetime.now()) + "] " +
                      "Destroying low priority session")
            print(stream)
            self.DestroySession(currentit)
            del self.__mSessions[currentkey]
        else:
            return False
        return True

    def NumActiveSessions(self):
        '''Retorna el numero de sesiones activas'''
        return len(self.__mSessions)

    def BindToSession(self, pClient, sessionKey):
        '''Asocia una sesion a un cliente, para ello la bloquea.
        Parametros:
        pCliente-- Cliente a asociar la sesion
        sessionKey-- Identificacion de la sesion'''
        pSession = self.GetSession(sessionKey)
        if pSession:
            if not pSession.Lock(pClient):
                stream = ("[" + str(datetime.now()) + "] " +
                          "Failed to lock session")
                print(stream)
                # force the old client to release the session?
                # this might be dangerous
                pSession.Unlock(pSession.GetLock())
                if pSession.Lock(pClient):
                    return pSession
                return None
            pSession.Touch()
        return pSession
