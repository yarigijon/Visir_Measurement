# coding=utf-8
# modulo creado para ser heredado y forzar a la clase hija al menos a tener implementados
#  estos metodos aunque solo retornen 0

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
    '''Objeto del que deben heredar todos los objetos autentificadores y que deben implementar
    como minimo.'''
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