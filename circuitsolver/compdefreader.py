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

# coding=utf-8
from stringop import*
from listparser import ComponentTypeDefinition

class ComponentDefinitionRegistry (object):

    def __new__(cls):
        # Implementacion especial del singleton
        if not hasattr(cls, 'instance'): # Si no existe el atributo 'instance'
            cls.instance = super(ComponentDefinitionRegistry, cls).__new__(cls) # lo creamos
        return cls.instance

    def Register (self):
        self.ComponentDefinition = None

    def AddComponentDefinition(self, ComponentDefinition):
        self.ComponentDefinition = ComponentDefinition

    def AddComponentList(self, ComponentList):
        self.ComponentList = ComponentList

    def GetComponentDefinition(self):
        return self.ComponentDefinition

    def GetComponentList(self):
        return self.ComponentList

class ComponentDefinitionReader (object):
    '''Clase para leer la lista de componentes'''
    __mCompDefs = []

    def ReadFile(self , filename):
        '''Funcion que dado un nombre de archivo lo lee y lo procesa linea a linea.
        Retorna verdadero cuando acaba de leer el archivo sin problemas, Falso en el caso
        de no poder abrir el archivo.
        Parametros:
        filename -- Path del archivo'''
        File = open(filename,"r") 
        if File.closed: # chequeamos que realmente se ha abierto el fichero
            return False
        line = File.readline() #leemos la primera linea
        while line: # mientras no eof
            if not self.IsComment(line):
                self.ParseLine(line)
            line = File.readline() #leemos la siguiente linea
        return True

    def IsComment(self, Line):
        '''Funcion que comprueba si una linea es un comentario o no
        Parametros:
        Line -- linea, cadena de texto, a procesar
        '''
        pos = find_first_not_of(Line , " \t\n")
        if pos != npos():
            if Line[pos] == "#" or Line[pos] == '*':
                return True
        else:
            return True # empty line, las lineas vacias se consideran comentarios
        return False
    
    def ParseLine(self, inLine):
        ''' Convierte la linea, cadena de texto, leida en un componente y lo añade
        a la lista de componentes. (variable privada de la clase).abs
        Parametros:
        inLine -- cadena de texto a procesar.
        '''
        pos = find_first_of(inLine, "#*")
        if pos != npos():
            Line = inLine[0:pos]
        else:
            Line = inLine
        tokens = []
        Type = ""
        numCons = 0
        hasSpecialValue = False
        ignoreValue = False
        canTurn = False
        tokens = Tokenize(Line, tokens, " \t", True)
        for i in range(0,len(tokens)):
            if i == 0:
                Type = ToUpper(tokens[0])
            elif i == 1:
                numCons = int(tokens[1])
            elif i == 2:
                flags = tokens[2]
                for j in range(0,len(flags)):
                    if flags[j]=="i" or flags[j]=="I":
                        ignoreValue = True
                    elif flags[j]=="s" or flags[j]=="S":
                        hasSpecialValue = True
                    elif flags[j]=="t" or flags[j]=="T":
                        canTurn = True
            else:
                return False
        self.__mCompDefs.append(ComponentTypeDefinition(Type, numCons, canTurn, ignoreValue, hasSpecialValue))
        return True

    def GetDefinitions(self):
        '''Retorna la lista de componentes'''
        return self.__mCompDefs 
        