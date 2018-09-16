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
from stringop import *
# General list component/entry/node.
class ListComponent(object):
   # Private
    __mConnections = []
    __mType = []
    __mName = []
    __mGroupID = None
    __mSpecial = []
    __mValue = None

    # Public
    def __init__(self, *arg):
        """Constructor para inicializar la clase list component.

        Parámetros:
        arg -- array variable que inicializa las variables privadas en funcion
        del tamaño de este   
        """
        self.__mConnections = []
        if len(arg) == 2:
            self.__mType = arg[0]
            self.__mName = arg[1]
            self.__mGroupID = 0
        elif len(arg) == 3:
            self.__mType = arg[0]
            self.__mName = arg[1]
            self.__mConnections.append(arg[2])
            self.__mGroupID = 0
	# ctor for standard 2 connection components..
        elif len(arg) == 4:
            self.__mType = arg[0]
            self.__mName = arg[1]
            self.__mConnections.append(arg[2])
            self.__mConnections.append(arg[3])
            self.__mGroupID = 0

    def Equals(self, other):
        """Funcion igual, compara un list component con otro.

        Devuelve verdadero si los elementos son iguales, es decir si
        el tipo y el valor de los dos elementos son iguales

        Parámetros:
        other -- variable que contiene un listcomponent
        """
        if  self.__mType == other.GetType() and self.__mValue == other.GetValue():
            return True
        return False

    def EqualsWithConnection(self, other):
        """Funcion igual, compara tipo y valor de 2 list conmponentes
        y en el caso de ser iguales además compara las conexiones

        Devuelve verdadero si tipo, valor y las conexiones son iguales, 
        falso en otro caso

        Parámetros:
        other -- variable que contiene un list component        
        """
        if self.__mType != other.GetType() or self.__mValue != other.GetValue():
            return False
        if self.__mConnections != other.GetConnections():
            return False
        return True

    def __eq__(self, other):
        """ Sobrecarga del operador igual, donde se comparan dos list components
        y se comprueba que todos sus elementos de son iguales

        Devuelve verdadero si todos los elementos de listComponent son iguales,
        falso en otro caso

        Parámetros:
        other -- variable que contiene un list component        
        """
        if self.Equals(other) == False:
            return False
        if self.__mName != other.GetName():
            return False
        if self.__mConnections != other.GetConnections():
            return False
        return True

    def __lt__(self, other):
        """ Sobrecarga del operador menor que, donde se comparan dos list components
        y se comprueba que alguno de los elementos es menor

        Devuelve verdadero si alguno de los elementos de listComponent es menor,
        falso en otro caso

        Parámetros:
        other -- variable que contiene un list component        
        """
        # sorting is done by combining the type and name of component..
        c1 = self.__mType + self.__mName + self.__mValue
        c2 = other.GetType() + other.GetName() + other.GetValue()
        if c1 < c2: 
            return True
        elif c2 < c1:   
            return False
        # else both are the same.. compare connections
        return self.__mConnections < other.GetConnections()

    #XXX: this info should come from the definition and not be hard coded
    def CanTurn(self):
        """ Método que indica si un componente puede ser girado o no.
        Elementos que se pueden girar: R, L, C, SHORTCUT, XSWITCHOPEN, XSWITCHCLOSE,
        IPROBE

        Devuelve verdadero si el elemento puede ser girado, falso en otro caso        
        """
        if self.__mType == "R":
            return True
        elif self.__mType == "L":
            return True
        elif self.__mType == "C":
            return True
        elif self.__mType == "SHORTCUT":
            return True
        elif self.__mType == "XSWITCHOPEN":
            return True
        elif self.__mType == "XSWITCHCLOSE":
            return True
        elif self.__mType == "IPROBE":
            return True
        return False

    def Dump(self):
        """ Método que crea y devuelve una cadena con los elementos del componente

        Devuelve un string con el contenido de todos los elementos del componente        
        """
        out = "Component: "
        if self.__mValue!=None:
            out += "'" + self.__mType + "' '" + self.__mName + "' '" + self.__mValue + "'"
        else:
            out += "'" + self.__mType + "' '" + self.__mName + "'"
        for it in range(len(self.__mConnections)):
            out += " " + self.__mConnections[it]
        return out   

    def GetConnections(self):
        """
        Devuelve un array con las conexiones del componente
        """
        return self.__mConnections

    def GetName(self):
        """ 
        Devuelve el nombre del componente
        """
        return self.__mName

    def GetType(self):
        """ 
        Devuelve el tipo del componente
        """
        return self.__mType

    def GetValue(self):
        """ 
        Devuelve el valor del componente
        """
        return self.__mValue

    def GetSpecial(self):
        """ 
        Devuelve verdadero si se trata de un componente especial,
        falso en otro caso
        """
        return self.__mSpecial  

    def AddConnection(self, con):
        """ 
        Añade una conexión al componente
        """
        self.__mConnections.append(con)

    def SetValue(self, value):
        """ 
        Añade el valor al componente
        """
        self.__mValue = value

    def SetType(self, newtype):
        """ 
        Añade el tipo al componente
                
        """
        self.__mType = newtype	

    def SetSpecial(self, special):
        """ 
        Marca el componente como especial (Verdadero)
                
        """
        self.__mSpecial = special

    def SetName(self, name):
        """ 
        Añade el nombre al componente
                
        """
        self.__mName = name   

    def IsInGroup(self):
        """ 
        Comprueba que el componente pertenece a un grupo
                
        """
        return self.__mGroupID != 0

    def GetGroup(self):
        """ 
        Devuelve el grupo del componente
                
        """
        return self.__mGroupID

    def SetGroup(self, groupid):
        """ 
        Añade el grupo al componente
                
        """
        self.__mGroupID = groupid

    def GetSpecialToken(self, name):
        """ 
        Devuelve el valor de elemento especial del componente
                        
        """
        # buscamos la primera aparicion del parametro pasado en name
        start = self.__mSpecial.find(name) # not found it return -1
        # si no lo encuentra devuelve cadena vacia
        if start == -1 or (start + len(name)) >= len(self.__mSpecial):
            return ""
        # en caso de encontrar algo, se busca el primer espacio en blanco
        # devolviendo la posicion de este, de esta manera tenemos donde empieza
        # y donde acaba el valor de la cadena especial que queremos
        end = find_first_of(self.__mSpecial," ", start)
        Len = 0
        # si no ha encontrado un espacio en blanco es porque la linea ya se ha acabado
        # entonces el tamaño a copiar en el string nuevo es tamaño total - donde empieza
        # - el tamaño del parametro: ejemplo:( VDC+6V_3	D	max:6	imax:0.5 ), name=MAX: mSpecial=max:6 
        # imax:0.5. Start:4 end=6 Len=1 
        if end == -1:
            Len = len(self.__mSpecial) - start - len(name)
        else:
            Len = end - start - len(name)
        if Len <= 0 :
            return ""
        return self.__mSpecial[start + len(name):Len + start + len(name)]