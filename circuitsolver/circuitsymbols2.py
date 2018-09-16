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
from basic_exception import *
cSymbolReverseLookup = "0ABCDEFGHI"

DEBUG_OUT = False # este debe ir en el main quitar de aqui una vez chequeado el modulo

class SymbolTable (object):
    ''''''
    def __init__(self):
        '''Constructor que inilicializa el vector mNodeToIdx a -1 y el
        __mSymbolsCounter a 0'''
        self.__mNodeToIdx=[0]*10
        self.__mSymbolCounter = None
        self.__sSymbolLookup = [] # Contiene el nombre de los simbolos, en visir original contiene estructuras name con tamaño max 16
        self.__mSymbolToNodeIdx = [] # Contiene el indice de todos los nodos
        for i in range(0, len(self.__mNodeToIdx)):
            self.__mNodeToIdx[i] = -1
        self.__mSymbolCounter = 0
    
    def Ref(self, sym1, sym2):
        '''Añade una referencia entre sym1 y sym2. Retorna falso si más de un
        nodo es definido en el vector de resultados de simbolos.
        Obtiene ambos simbolos, si ambos existen, los mezcla y actualiza el indice.
        Parametros:
        sym1 -- Simbolo 1
        sym2 -- Simbolo 2'''
        idx1 = self.GetIndexOf(sym1)
        idx2 = self.GetIndexOf(sym2)
        if idx1 != -1 and idx1 == idx2: # Son iguales?
            return True
        if idx1 >= 0 and idx2 >= 0: # son los dos distintos de -1? Es decir existian en el vector los dos
            if idx1 < idx2:
                if self.MergeNodes(idx1, idx2, sym2) == False:
                    return False
            else:
                if self.MergeNodes(idx2, idx1, sym1) == False:
                    return False
        elif idx1 >= 0: # existia en el vector el primero
            self.GetSymbolRef(sym2, idx1)
        elif idx2 >= 0: # existia en el vector el segundo
	        self.GetSymbolRef(sym1, idx2)
        else: # no existia ninguno de los dos
            newindex = self.CreateNode() # creamos un nuevo nodo
            self.GetSymbolRef(sym1, newindex)
            self.GetSymbolRef(sym2, newindex)
        return True
    
    def Insert(self, sym, node):
        '''Busca el simbolo y añade el nodo a él.
        Si el nodo existe en otra parte, retornara False
        Parametros
        sym -- simbolo
        node -- nodo
        NOTA: No se puede devolver sólo false si el nodo está
         definido en otro lugar ya que la función se utiliza con o sin verificación'''
        # finds the symbol and adds the node to it
        # if the node exists elsewhere, it will return false
        # Notice: Can't just return false if the node is defined elsewhere as the function
        #  is used with or without verification
        self.ValidateNodeName(node)
        idx = self.GetIndexOf(sym)
        rv = True
        if idx < 0:
            newindex = self.CreateNode(node[0])
            if (newindex < 0):
                return False
            self.GetSymbolRef(sym, newindex)
        else:
            value = self.AddNodeToIdx(idx, node[0]) 
            return value >= 0
        return rv

    def Remove(self, sym):
        ''' Borrar el simbolo y los nodos asociados al simbolo.
        Parametros:
        sym -- Simbolo a borrar
        '''
        self.EraseNodeForSymbol(sym)
        self.EraseSymbol(sym)

    def ContainsSymbolOrEmpty(self, sym, node):
        ''' Funcion que devuelve verdadero en caso de que el simbolo o bien
        no exista o bien no haya ningun nodo definido con ese nodo
        Parametros:
        sym -- simbolo a buscar
        node -- vector con los nodos
        '''
        self.ValidateNodeName(node)
        idx = self.GetIndexOf(sym)
        if idx < 0:
            return True
        if self.NodesUsedForIdx(idx) == 0:
            return True
        return self.IdxUsesNode(idx, node[0])

    def ContainsSymbol(self, sym, node):
        '''Funcion que comprueba que un simbolo esta dentro del array de simbolos
        o asociado a un nodo.
        Parametros:
        sym -- simbolo a buscar.
        node -- nodo'''
        self.ValidateNodeName(node)
        idx = self.GetIndexOf(sym)
        if idx < 0:
            return False
        return self.IdxUsesNode(idx, node[0])

    def IsUsed(self, sym):
        '''Indica si el simbolo es usado en algun nodo  o no.
        Parametros:
        sym -- simbolo a buscar'''
        idx = self.GetIndexOf(sym)
        if idx >= 0:
            return self.NodesUsedForIdx(idx) > 0
        return False
    
    def RefersSameSymbol(self, sym1, sym2):
        '''Indica si los simbolos son el mismo o no
        Parametros:
        sym1 -- simbolo 1
        sym2 -- simbolo 2'''
        idx1 = self.GetIndexOf(sym1)
        idx2 = self.GetIndexOf(sym2)
        if idx1 >= 0 and idx2 >= 0 and idx1 == idx2:
            return True
        return False
    
    def RefersSameNode(self, node1, node2):
        '''Indica si dos nodos son iguales o no (apuntan al mismo simbolo)
        Parametros:
        node1 -- nodo 1
        node2 -- nodo 2'''
        self.ValidateNodeName(node1)
        self.ValidateNodeName(node2)
        idx1 = self.FindNodeIdx(node1[0])
        idx2 = self.FindNodeIdx(node2[0])
        if idx1 >= 0 and idx2 >= 0 and idx1 == idx2:
            return True
        return False
    
    def GetFirstNodeOrSpare(self, sym):
        '''Funcion usada por los instrumentos para obtener el primer
        nombre de nodo usado o un nodo libre sino esta definido, devuelve
        "NOSPARE" si no hay nodos libres.
        Parametros:
        sym -- simbolo a asociar con el nodo
        '''
        out = ""
        idx = self.GetIndexOf(sym)
        if idx >= 0:
            out = self.GetFirstNodeForIdx(idx)
        if out !="":
            return out
        allowedNodes = "ABCDEFGHI"
        allowed = set(allowedNodes)
        used = set()
        for i in range(0,len(self.__mNodeToIdx)):
            if self.__mNodeToIdx[i] > -1:
                used.add(cSymbolReverseLookup[i])
        diff = allowed.difference(used)
        if not diff:
            return "NOSPARE"
        strout = list(diff)
        self.Insert(sym, strout[0])
        return strout[0]
        
    def Mark(self, markdata, sym):
        '''Marca el indice de un simbolo
        Parametros:
        markdata -- conjunto con los indices de los simbolos marcados
        sym -- simbolo a marcar'''
        # should this create the node if it doesn't exist?
        idx = self.GetIndexOf(sym)
        if idx >= 0:
            markdata.add(idx)
        else:
            newindex = self.CreateNode()
            markdata.add(newindex)
            self.GetSymbolRef(sym, newindex)
        return markdata
    
    def IsMarked(self, markdata, sym):
        '''Devuelve verdadero si el simbolo esta marcado falso en otro caso
        Parametros:
        markData -- conjunto con los symbolos marcados
        sym -- simbolo del que queremos saber si esta marcado'''
        idx = self.GetIndexOf(sym)
        if idx >= 0:
            return idx in markdata
        return False

    def ToSymbolName(self, symbol): #eliminado out ya que solo es para el return
        '''Basicamente comprueba si la longitud en caracteres es superior a 16
         si lo es devuelve <INVALID>
         Parametros:
         symbol -- nombre del simbolo a comprobar'''
        if len(symbol) >= 16:
            invalid = "<INVALID>"
            return invalid
        else:
            return symbol

    def LookupSymbol(self, symbol):
        '''Tenemos el nombre de un simbolo y recorremos vector self.__sSymbolLookup para ver si ya se ha almacenado
         el nombre y obtener asi su indice de no existir retornamos -1.
         Parametro:
         symbol -- nombre a buscar'''
        for i in range(0, len(self.__sSymbolLookup)): # Recorremos todo el vector
            if symbol == self.__sSymbolLookup[i]: # si existe 
                return i # se retorna el indice
        return -1 # de lo contrario -1

    # hemos visto que en visir original cuando se iguala un metodo a un valor
    # equivale a cambiar el valor de la variable que retorna, como no lo podemos ahcer en python
    # pasamos dos parametros en ese caso
    def GetSymbolRef(self, *arg):
        ''' Retorna el valor del simbolo 
        Parametros:
        *arg -- argumento de longitud variable, tamaño uno es el simbolo a a buscar
        tamaño dos es el simbolo a buscar y el indice por el cual sustituir
        '''
        symbol = arg[0]
        if len(arg) == 2:
            newvalue = arg[1]
        idx = self.LookupSymbol(symbol)
        if idx >= 0:
            if len(arg) == 2:
                self.__mSymbolToNodeIdx[idx] = newvalue
            return self.__mSymbolToNodeIdx[idx]
        symname = self.ToSymbolName(symbol) #comprueba que es mayor de 16
        newidx = len(self.__sSymbolLookup)
        self.__sSymbolLookup.append(symname) # añadimos al vector
        if len(self.__mSymbolToNodeIdx) <= newidx:
            while len(self.__mSymbolToNodeIdx)<=(newidx+1)*2: # python no tiene resize asi que lo hacemos nosotros, añadimos None
                self.__mSymbolToNodeIdx.append(0)
        self.__mSymbolToNodeIdx[newidx] = -1
        if len(arg)==2:
            self.__mSymbolToNodeIdx[newidx] = newvalue
        return self.__mSymbolToNodeIdx[newidx]
    
    @staticmethod
    def ResetLookup():
        '''Resetea el vector sSymbolLookup'''
        SymbolTable.__sSymbolLookup = []

    def GetIndexOf(self, sym):
        '''Retorna el indice del simbolo a buscar.
        Parametros:
        sym -- simbolo a buscar'''
        idx = self.LookupSymbol(sym)
        if idx < 0: # Si no existia
            return -1 # Retornamos -1
        return self.__mSymbolToNodeIdx[idx] # Retornamos el nodo

    def UpdateRef(self, ref, newref):
        '''Sustituye en el vector mSymboToNodeIdx toda posicion que coincida
        con la antigua referencia por la nueva.        
        Parametros:
        ref -- antigua referencia
        newref -- nueva referencia
        '''
        assert(ref != -1 and "ref can't be -1")
        assert(newref != -1 and "newref can't be -1")
        for i in range(0,len(self.__mSymbolToNodeIdx)):
            if (self.__mSymbolToNodeIdx[i] == ref):
                self.__mSymbolToNodeIdx[i] = newref
    
    def EraseSymbol(self, symbol):
        '''Borra el symbolo, poniendo la posicion de ese simbolo a -1
        Parametros:
        symbol -- simbolo a elminar.'''
        self.GetSymbolRef(symbol, -1)
    
    def DumpSymbols(self):
        '''Retorna  la cadena con los nombres de los simbolos y su correspondiente indice'''
        outbuffer = ""
        for i in range(0, len(self.__sSymbolLookup)):
            outbuffer = outbuffer + "(" + str(self.__sSymbolLookup[i]) + "-" + str(self.__mSymbolToNodeIdx[i]) + ") "
        return outbuffer
    
    def ValidateNodeName(self, node):
        '''Valida que el nombre del nodo solo sea una letra
        Parametro: 
        node -- nombre del nodo'''
        if len(node) > 1:
            raise BasicException("Invalid node name found in symboltable")

    def FindNodeIdx(self, node):
        '''Busca si un nodo particular es usado y retorna el indice.
        Parametros:
        node -- nodo a buscar'''
        # look if perticular node is used somewhere and return the index
        nodeid = self.LookupNode(node)
        return self.__mNodeToIdx[nodeid]

    def MergeNodes(self, dst, src, srcsym):
        '''Cambia el indice del nodo desde src a dst, es decir, busca el indice dentro
        del vector de simbolos que coincide con src y lo cambia por dst, tambien lo cambia en
        el vector de simbolos asociado al nombre
        Parametros:
        dst -- index destino
        src -- index fuente
        srcsym --
        '''
        for i in range(0,len(self.__mNodeToIdx)):
            if self.__mNodeToIdx[i] == src:
                self.__mNodeToIdx[i] = dst
        self.GetSymbolRef(srcsym, dst)
        self.UpdateRef(src, dst)
        if self.NodesUsedForIdx(dst) > 1:
            return False
        return True
    
    def CreateNode(self, *arg):
        '''Dos tipos de create node, sin parametros que lo unico que hace es
        aunmentar en 1 el mSymbolCounter
        Y la otra que se pasa por parametro el node, busca si tiene simbolos asociados
        entonces aument el numero de simbolos de ese nodo, o en el caso que no tenga simbolo
        asociado devuelve -1
        Parametros:
        node -- nodo a buscar'''
        if len(arg) == 0:
            mSymbolcounterPreReturn = self.__mSymbolCounter
            self.__mSymbolCounter = self.__mSymbolCounter + 1
            return mSymbolcounterPreReturn
        node = arg[0]
        nodeid = self.LookupNode(node)
        if self.__mNodeToIdx[nodeid] >= 0:
            return -1 # used elsewhere
        newSym = self.__mSymbolCounter # primero asignamos
        self.__mSymbolCounter = self.__mSymbolCounter + 1 # Despues incrementamos en 1
        self.__mNodeToIdx[nodeid] = newSym
        return newSym
    
    def AddNodeToIdx(self, idx, node):
        ''' Comprueba si el nodo esta siendo usado, devolviendo el indice del simbolo, 
        si es distinto del index del simbolo es que esta siendo usado por otro o que no esta
        siendo usado por nadie (-1) entonces lo asociamos al indice del simbolo y retornamos
        el indice.
        Parametros:
        idx --  indice del simbolo a buscar
        node -- nodo 
        '''
        nodeid = self.LookupNode(node)
        if idx == self.__mNodeToIdx[nodeid]:
            return idx # we're already using the node, ok
        if self.__mNodeToIdx[nodeid] != -1:
            return -1 # someone else is using this node        
        self.__mNodeToIdx[nodeid] = idx
        return idx
    
    def DumpNodes(self):
        '''Retorna una cadena con el indice del nodo y el nombre de este'''
        out = ""
        for i in range(0,len(self.__mNodeToIdx)):
            if self.__mNodeToIdx[i] > -1:
                out = out + "(" + str(self.__mNodeToIdx[i]) + ") " + str(cSymbolReverseLookup[i]) + " "
        return out

    def ReverseLookupNode(self, i):
        '''Devuelve el valor del nodo indicado por i del vector cSymbolReverseLookup
        Parametros:
        i -- indice a buscar'''
        if (i >= len(self.__mNodeToIdx)):
            raise BasicException("Out of bounds in ReverseLookupNode")
        return cSymbolReverseLookup[i]

    def LookupNode(self, node):
        ''' Retorna el valor entero del node. Se calcula
        el valor ascii del nodo menos el valor ascii de A más uno.
        Parametro:
        node -- nodo a comprobar
        '''
        if node >= 'A' and node <= 'I':
            return ord(node) - ord('A') + 1
        if node == '0':
            return 0
        raise BasicException("Invalid node name found in symboltable node lookup")
        return 0 # never reached

    def EraseNodeForSymbol(self, sym):
        '''Borra del vector de mNodeToIdx la relacion con el simbolo.
        Parametros:
        sym -- simbolo a buscar, del que se borraran todos los nodos'''
        idx = self.GetIndexOf(sym)
        if idx >= 0:
            for i in range(0,len(self.__mNodeToIdx)):
                if self.__mNodeToIdx[i] == idx:
                    self.__mNodeToIdx[i] = -1
                
    def NodesUsedForIdx(self, idx):
        '''Esta funcion retorna el numero de nodos que coincide con ese index
        que a su vez representa un simbolo.
        Parametros:
        idx -- indice del vector de simbolos a buscar'''
        usage = 0
        for i in range(0,len(self.__mNodeToIdx)):
            if self.__mNodeToIdx[i] == idx:
                usage = usage + 1
        return usage
    
    def IdxUsesNode(self, idx, node):
        '''Retorna verdadero si el indice del vector simbolos coincide con
        el de nodos.
        Parametros:
        idx -- indice dentro del array de simbolos que representa el simbolo
        node -- node 
        '''
        nodeid = self.LookupNode(node)
        return self.__mNodeToIdx[nodeid] == idx
    
    def GetFirstNodeForIdx(self, idx):
        '''
        Parametros:
        idx -- indice del vector de simbolos a buscar'''
        for i in range(0,len(self.__mNodeToIdx)):
            if self.__mNodeToIdx[i] == idx:
                return self.ReverseLookupNode(i)
        return ""
