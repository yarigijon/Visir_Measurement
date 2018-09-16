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
from listcomponent import ListComponent

class ListAlgorithm(object):
    """Clase auxiliar para la operacion con listas.
    Hacer operaciones y buscar nodos
    
    """
    __mNodeList= [] # private

    # public
    @staticmethod
    def MatchNode(comp, lista, out):
        ''' Busca en list si existe algun component igual al definido con comp.SetType
        y comp.SetValue y conections en el codigo se utiliza para buscar
        en la lista puentes (shortcut)
        
        Parametros:
        comp -- component a buscar
        lista -- lista donde se busca el componente
        out -- ¿quitar? es el retorno reminiscencia del c++
        '''
        for it in lista:
            if comp.EqualsWithConnection(it):
                out = it
                return out, True
        out = it
        return out, False
    
    @staticmethod
    def IsSubsetOf(subset, superset):
        '''Dados dos conjuntos, este metodo retorna verdadero si es un subconjunto del
        superconjunto pasado tambien parametro.

        Parametros:
        subset -- subconjunto de nodos a buscar
        superset -- lista donde se busca el componente
        '''
        matchlist = []
        matchlist, out = ListAlgorithm.Match(subset, superset, matchlist)
        return out
    
    @staticmethod
    def IsSubsetOfWithFailed(subset, superset, failed):
        '''Dados dos conjuntos comprueba que todo el subconjunto este dentro del superconjunto
        Retorna un vector con aquellos nodos que no forman parte del superconjunto (de la max list,creo)
        y False en caso de que el vector contenga algún nodo.

        Parametros:
        subset -- subconjunto de nodos a buscar
        superset -- lista donde se busca el componente
        failed -- Lista de nodos del subset que no se encuentran en el super conjunto
        '''
        matchlist = []
        rv = True
        for it in subset:
            matchlist, out =ListAlgorithm.TestSubNode(matchlist, superset, it)
            if out == False:
                failed.append(it)
                rv = False
        return failed, rv
    
    @staticmethod
    def Match(subset, superset, out):
        '''Recorre un subconjunto de nodos y comprueba que todos y cada uno de ellos
        esta dentro de un superconjunto. 
        Retorna una lista con todos aquellos nodos encontrados, y verdadero en caso de que
        todo el subconjunto este contenido. Falso en otro caso.

        Parametros:
        subset -- subconjunto de nodos a buscar
        superset -- lista donde se busca el componente
        out -- ¿quitar? es el retorno reminiscencia del c++
        '''
        out = []
        for it in subset:
            out, bolean = ListAlgorithm.TestSubNode(out, superset, it)
            if bolean == False:
                return out, False
        return out, True

    @staticmethod
    def TestSubNode( matchlist, superset, comp):
        '''Comprueba que un nodo (list component) esta contenido y es exactamente igual (incluidas
        conexiones) a otro dentro del superconjunto
        Retorna un array donde se van almacenando los nodos coincidentes del subconjunto y verdadero.
        Falso en caso de que no este contenido en el superconjunto
        
        Parametros:
        machlist -- lista con los nodos encontrados
        superset -- lista donde se busca el componente
        comp -- componente a buscar
        '''
        for it in superset:
            # check if the nodes match
            if comp.EqualsWithConnection(it):
                # and the node is not already used
                try:
                    matchlist.index(it)
                except:
                    matchlist.append(it)
                    return matchlist, True
        return matchlist, False

    @staticmethod
    def MatchIndex(subset, superset,  out):
        '''Retorna un vector de pares que contiene el indice del superconjunto y
        el indice del subconjunto donde ambos nodos coincidente
        Además retornara verdadero en caso de encontrar el subconjunto dentro del superconjunto
        falso en el primer momento que un elemento del subconjunto no este dentro del superconjunto

        Parametros:
        subset -- subconjunto de nodos a buscar
        superset -- lista de componentes
        out -- ¿sobra? viene del c++ porque se cambia por referencia
        '''
        out = []
        used = [0]*len(superset) #inicializamos used con tantos 0 como tamaño tiene superset
        for subi in range(0,len(subset)):
            matched = False
            for superi in range(0,len(superset)):
                if matched:
                    break
                if used[superi]==0 and subset[subi].EqualsWithConnection(superset[superi]):
                    matched = True
                    used[superi] = 1
                    pair = (superi, subi)
                    out.append(pair)
            if not(matched):
                out= []
                return out, False
        return out, True

    @staticmethod
    def Replace(comp, lista, replace, out):
        '''Busca componentes con el mismo tipo y valor y los remplaza con
        componentes de la lista de reemplazo
        Retorna la lista con los remplazos

        Parametros:
        comp -- componente con el que se realizara la comparacion
        lista -- lista de componentes
        replace -- lista de componentes usados en el remplazo
        out -- todo ¿quitar? reminiscencias del c++
        '''
        out = []
        for it in lista:
            if comp.Equals(it):
                for repit in replace:
                    out.append(repit)
            else:
                out.append(it)
        return out

    @staticmethod
    def ReplaceNamed(name, lista, comp):
        '''Busca componentes por el nombre y lo remplaza por otro.
        Retorna la lista de componentes modificada.

        Parametros:
        name -- nombre a buscar
        lista -- lista de componentes
        comp -- componente usado como remplazo
        '''
        for i in range(0, len(lista)):
            if lista[i].GetName() == name:
                lista[i]=comp
        return lista

    @staticmethod
    def ReplaceTypeWithList(name, lista, replace):
        '''Busca componentes por el tipo y lo remplaza por otro o una lista de otros.
        Retorna la lista de componentes modificada.

        Parametros:
        typea -- tipo a buscar
        lista -- lista de componentes
        replace -- lista con los nodos a remplazar
        '''
        out=[]
        for it in lista:
            if it.GetType() == name:
                for repit in replace:
                    out.append(repit)
            else:
                out.append(it)
        return out

    @staticmethod
    def ReplaceType(typea, lista, newtype):
        '''Busca componentes por el tipo y lo remplaza por otro o una lista de otros.
        Retorna la lista de componentes modificada.

        Parametros:
        typea -- tipo a buscar
        lista -- lista de componentes
        newtype -- nuevo tipo
        '''
        for i in range(0, len(lista)):
            if typea == lista[i].GetType():
                lista[i].SetType(newtype)
        return lista

    @staticmethod
    def PushNodesOfType(typea, lista, out):
        '''Busca nodos de un tipo en la lista
        Retorna un vector/lista con los nodos que coinciden con ese tipo

        Parametros:
        typea -- tipo a buscar
        lista -- lista de componentes
        '''
        out = []
        for it in lista:
            if typea == it.GetType():
                out.append(it)
        return out

    @staticmethod
    def RemoveOfType(typea, out):
        '''Metodo que elimina todos los nodos de un tipo de la lista.

        Retorna un array con todos los nodoes excepto los del tipo pasado
        en typea como parametro.

        Parametros:
        typea -- Tipo de nodo a borrar.
        out -- lista que contiene los nodos.
        '''
        temp = []
        for it in out:
            if typea != it.GetType():
                 temp.append(it)
        return temp

    @staticmethod
    def CircuitSetupMatch(inCircuit, compList, out):
        '''Metodo que limpia la netlist para despues buscar en ella,
        netlist menos las sondas de los intrumentos que son eliminados
        o renombrados porque no afecta a la resolucion del circuito.

        Retorna la lista con los nodos que cumplen los requisitos y verdadero en caso
        de encontrarlos. Falso en otro caso.

        Parametros:
        inCircuit -- Lista con los nodos del circuito
        comList -- Lista con los componentes
        out -- Lista con los componentes que cumplen las especificaciones (es el retorno,
        para que se parezca a lo que hay en C)
        '''
        nodes = inCircuit # copy
        # Clean up netlist for matching
        # Remove instruments and convert/remove switches
        nodes = ListAlgorithm.RemoveOfType("DMM", nodes)
        nodes = ListAlgorithm.RemoveOfType("IPROBE", nodes)
        nodes = ListAlgorithm.RemoveOfType("PROBE1", nodes)
        nodes = ListAlgorithm.RemoveOfType("PROBE2", nodes)
        nodes = ListAlgorithm.RemoveOfType("PROBE3", nodes)
        nodes = ListAlgorithm.RemoveOfType("PROBE4", nodes)
        # un swich close es un cortocircuito  ¿esta negado?
        # TODO: Comprobar en la web
        nodes = ListAlgorithm.RemoveOfType("XSWITCHCLOSE", nodes)
        nodes = ListAlgorithm.ReplaceType("XSWITCHOPEN",  nodes, "SHORTCUT")

        return ListAlgorithm.Match(compList,nodes, out)
