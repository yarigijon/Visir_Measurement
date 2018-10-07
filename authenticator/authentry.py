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
# modulo creado para ser heredado y forzar a la clase hija
# al menos a tener implementados estos metodos aunque solo retornen 0


class IAuthEntry(object):
    '''Objeto "padre" que define las caracteristicas minimas que tiene que tener
    un objeto de autentificacion'''
    def GetCookie(self):
        '''Retorna la cookie asociada al objeto de autentificacion'''
        return 0

    def GetIP(self):
        '''Retorna la IP del autenficador'''
        return 0

    def GetTimeout(self):
        '''Retorna el timeout del objeto autentificador'''
        return 0

    def GetPrio(self):
        '''Retorna la prioridad'''
        return 0

    def SetCookie(self, cookie):
        '''Asocia la cookie.
        Parametros:
        cookie -- la cookie a asociar'''
        return 0

    def SetIP(self, ip):
        '''Asocia la ip.
        Parametros:
        ip-- la IP a asociar'''
        return 0

    def SetTimeout(self, timeout):
        '''Asocia el timeout.
        Parametro:
        timeout-- tiempo a asociar'''
        return 0

    def SetPrio(self, prio):
        '''Asocia la prioridad.
        Parametro:
        prio -- Prioridad a asociar'''
        return 0


class ICredentials(object):
    ''''''
    def GetCookie(self):
        '''Retorna la cookie asociada'''
        return 0


class IAuthenticator(object):
    '''Objeto del que deben heredar todos los objetos autentificadores y
       que deben implementar como minimo.'''
    def Init(self):
        '''Constructor que inicia el autentificador'''
        return 0

    def FetchAuthEntry(self, pInCred, pOutAuthEntry, cacheId):
        ''' Ejecuta el metodo de autentificacion
        Parametros:
        pInCred-- ICredentials
        pOutAuthEntry-- IAuthEntry
        cacheId-- Identificador de cache'''
        return 0
