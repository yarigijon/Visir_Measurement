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
from ostreams import*
from circuitsymbols2 import SymbolTable
from listcomponent import ListComponent
import NamedNodes
import sys
import collections

instrumentNodes = ["VFGENA", "DMM", "PROBE", "PROBE1", "PROBE2", "PROBE3", "PROBE4", "VDC+25V", "VDC-25V", "VDC+6V", "VDCCOM"]
numInstrumentNodes = len(instrumentNodes)

def isInstrumentNode(Type):
    '''Metodo que dado un tipo devuelve true si se trata de un nodo de tipo instrumento
    falso en otro caso.
    Parametros:
    type -- tipo a comprobar'''
    for i in range(0, numInstrumentNodes):
        if Type in instrumentNodes:
            return True
    return False

class CircuitSolver3 (object):
    '''Clase que resuelve los circuitos'''
    def __init__(self):
        self.__mCircuit = [] # esto sera un vector de objetos listcomponent
        self.__mSolution = [] # esto sera un vector de objetos listcomponent
        self.__mSymbols = SymbolTable()
        self.__mSolutionSymbols = SymbolTable()
        self.__mCandCache = []
        self.__mIndexCircuit = []
        self.__mCandidates = []
        self.__mMeasInstrument = []
        self.__mShortcuts = []

    def Solve(self, incircuit, candidates):
        '''Funcion que resuelve el circuito
        Parametros:
        incircuit -- circuito 
        candidates -- lista de candidatos'''
        self.__mCircuit = [] # esto sera un vector de objetos listcomponent
        self.__mSolution = [] # esto sera un vector de objetos listcomponent
        self.__mSymbols = SymbolTable()
        self.__mSolutionSymbols = SymbolTable()
        self.__mCandCache = []
        self.__mIndexCircuit = []
        self.__mCandidates = []
        self.__mMeasInstrument = []
        self.__mShortcuts = []
        self.__mCircuit = incircuit
        self.__mSolution = [] # clear the vector
        SymbolTable.ResetLookup() # Igual debe ser la funcion estatica para poder llamarla sin crear objeto
        circuit = collections.deque()
        for it in self.__mCircuit: # hacemos esto porque python es demasiado listo y se adapta el tipo si igualamos o 
                                   # copiamos __mcircuit directamente ya que uno es tipo list y el otro deque
            circuit.append(it)
        circuit = self.CircuitFixup(circuit)
        self.InstrumentFixup(circuit)
        cleancirlist = collections.deque()
        instrSymbols = [] # * 16 # reservamos en el vector 16 posiciones
        used = [False] * len(circuit) # reservamos en el vector las mismas posiciones que tiene circuit
        ordered = []# * len(circuit) # reservamos en el vector las mismas posiciones que tiene circuit
        for i in range(len(circuit)):
            self.__mCandCache.append([])
        used, ordered, instrSymbols, bolean = self.TierOne(circuit, used, ordered, instrSymbols)
        cerr = OStream(sys.stderr)
        if not bolean:
            cerr << "Tier one failed" << endl
            return False
        # this needs the original circuit for the wires.
        # and the cleancirlist for adding components and removing wires when done
        # no retorno self.__mSymbols porque es de la propia clase
        used, instrSymbols, bolean = self.TierTwo(circuit, used, self.__mSymbols, instrSymbols)
        if not bolean:
            cerr << "Tier two failed" << endl
            return False
        for it in ordered:
            if it != None:
                if used[it]:
                    cleancirlist.append(circuit[it])
        boolean, usage = self.TierThree(cleancirlist, candidates, self.__mSymbols)
        if not boolean:
            return False
        self.AddInstrumentNodes(self.__mSolution)
        return True

    def InstrumentFixup(self, cand):
        ''' Insert instrument nodes for old "magic" node names
        Retorna la lista de candidados añadiendoles los que se listan a
        continuacion:
        FGEN_A => FGEN_1 FGEN_A
	    DMM_VHI, DMM_VLO => DMM_1 DMM_VHI DMM_VLO
	    OSC_1 => PROBE_1_1 OSC_1
	    OSC_2 => PROBE_1_2 OSC_2
	    OSC_3 => PROBE_1_3 OSC_3
	    OSC_4 => PROBE_1_4 OSC_4
	    DC_+25V => VDC+25V_1 DC_+25V
	    DC_-25V => VDC-25V_1 DC_-25V
	    DC_+6V => VDC+6V_1 DC_+6V
	    DC_COM => VDCCOM_1 DC_COM
        Parametros:
        cand -- vector de candidatos a añadir
        '''
        cand.append(ListComponent("VFGENA", "1", "FGEN_A"))
        cand.append(ListComponent("DMM", "1", "DMM_VHI", "DMM_VLO"))
        cand.append(ListComponent("PROBE1", "1", "OSC_1"))
        cand.append(ListComponent("PROBE2", "1", "OSC_2"))
        cand.append(ListComponent("PROBE3", "1", "OSC_3"))
        cand.append(ListComponent("PROBE4", "1", "OSC_4"))
        cand.append(ListComponent("VDC+25V", "1", "DC_+25V"))
        cand.append(ListComponent("VDC-25V", "1", "DC_-25V"))
        cand.append(ListComponent("VDC+6V", "1", "DC_+6V"))
        cand.append(ListComponent("VDCCOM", "1", "DC_COM"))
        self.SetSymbol("FGEN_A", "A")
        self.SetSymbol("0", "0")
        return cand

    def CircuitFixup(self, circuit):
        '''Añade a circuit elementos ocultos al circuito
        Parametros:
        circuit -- circuito donde añadir list componentes'''
        # Add (old) hidden instrument components to the circuit
        circuit.append(ListComponent(NamedNodes.DmmIProbe, "1", "DMM_AHI", "DMM_ALO"))
        return circuit

    def TierOne(self, cand, used, ordered, instrSymbols):
        '''
        Este metodo implementa la primera capa del algoritmo del circuit solver,
        lo que realiza es comprobar que todos los componentes estan conectados y no existen componentes sin usar
        Parametros:
        cand -- vector de candidatos
        used -- vector de usados
        ordered -- vector ordenado
        instrSymbols -- vector 
        '''
        toVisit = collections.deque()
        # Add all instrument nodes as nodes to visit
        # and keep track of the instruments
        # all connection names are symbolic
        for it in cand: # leemos una a una las lineas del circuito de entrada
            if isInstrumentNode(it.GetType()): # Si esa linea se trata de un instrumento
                cons = it.GetConnections() # extraemos sus conexiones
                for conit in cons: 
                    toVisit.append(conit) # añadimos conexion a la lista de conexiones a visitar
                    instrSymbols.append(conit) # añadimos la conexion a la lista de instrument symbols
        nodesToVisit = [ "0" ] # creamos un nodo "0" GND de algunos instrumentos
        numNodes = len(nodesToVisit)
        toVisit.extend(nodesToVisit) # añadimos el nodo "0" a la lista de conexiones a visitar
        while toVisit: # chequea  que el deque(lista que extraemos por los dos extremos) no esta vacio
            current =  toVisit.popleft() # extaemos de la lista de conexiones a visitar el primer elemento por la izq
            for candidx in range(0,len(cand)): # Vamos recorriendo linea a linea el circuito de entrada
                found = False # inicializamos variable porque no hemos encontrado una conexión de instrumento aun en el circuito
                if (used[candidx]): # Si ya hemos detectado la linea como conexion con instrumento anteriormente continuamos
                    continue
                cons = cand[candidx].GetConnections() # Para la linea actual extraemos las conexiones
                # check each component for any connection matching current symbol
                for conidx in range(0,len(cons)): #chequeamos para el componente de la linea actual que alguna si alguna de sus conexiones
                    if cons[conidx] == current:   #coincide con la del instrumento actual que estamos buscando
                        if len(cons) == 1: # si solo tiene una conexion
                            found = True # si coincide hemos encontrado una conexión del instrumento
                        # add all other connection points to the list of symbols to visit
                        for i in range(0,len(cons)): # si tiene mas de una conexion, añadimos los otros puntos de conexion a la lista de conexiones a visitar
                            if i != conidx:
                                # odd/old behaviour, count components directly connected to itself as not connected
                                if cons[i] != cons[conidx]: # se considera los componentes conectados a si mismo como no conectados
                                    toVisit.append(cons[i])
                                    found = True 
                if found: # si lo ha encontrado
                    used[candidx] = True # ponemos a True la linea equivalente en used
                    ordered.append(candidx) #guardamos el numero de linea en ordered
        return used, ordered, instrSymbols, True #instrSymbols contiene el nombre de las conexiones de los instrumentos

    def MarkWiresAsRefs(self, candidates, symbols):
        ''' Marca los cables como referencias
        Parametros:
        candidates -- Vector con los candidatos
        symbols -- Tabla de simbolos'''
        # insert wires from original list. That makes probes work
        for it in candidates:
            if it.GetType() == "W":
                # add ref and check that no symbol contains more than one nodename
                if not symbols.Ref(it.GetConnections()[0], it.GetConnections()[1]):
                    return False
        return True

    def TierTwo(self, List, usedcmpnts, symbols, usedInstrumentNodes):
        ''' Resuelve la capa 2
        Parametros:
        List -- lista de componentes Circuito a analizar
        usedcmpnts -- Vector de componentes usados
        symbols -- Tabla de simbolos
        usedInstrumentNodes -- vector de intrumentos usados
        '''
        if not self.MarkWiresAsRefs(List, symbols):
            return usedcmpnts, usedInstrumentNodes, False
        markData = set()
        for i in range(0,len(List)):
            if not usedcmpnts[i]:
                continue
            component = List[i]
            if component.GetType() != "W" and not isInstrumentNode(component.GetType()):
                cons = component.GetConnections()
                for it in cons: # en visir original llama i a este y al for anterior lo he cambiado por it, revisar si es correcto
                    symbols.Mark(markData, it)
        usedInstrumentNodes.append("0") # verify that this actually does the right thing..
        size = len(usedInstrumentNodes)
        for i in range(0,size):
            for j in range(i+1,size):
                if symbols.RefersSameSymbol(usedInstrumentNodes[i], usedInstrumentNodes[j]): # terminales instrumento unidos entre si?
                    symbols.Mark(markData, usedInstrumentNodes[i])
        size = len(List)
        for i in range(0,size):
            if not usedcmpnts[i]:
                continue
            Cmp = List[i]
            Type = Cmp.GetType()
            if Type == "W":
                usedcmpnts[i] = False
            elif isInstrumentNode(Type):
                # for now, just delete the probe and dmm nodes..
                used = True
                cons = Cmp.GetConnections()
                for ci in range(0,len(cons)):
                    if cons[ci] == "0": # < instruments connected to node "0" usually never connect the node directly
                        continue
                    if not symbols.IsMarked(markData, cons[ci]):
                        used = False
                if not used:
                    for it in cons:
                        symbols.Remove(cons[ci])
                    usedcmpnts[i] = False
                else:
                    # measurement instruments are in use, but we don't want them in the input circuit
                    # we still need to keep track of them so we can insert them after the circuit is solved
                    if Type == "DMM" or Type == "PROBE"or Type == "PROBE1" or Type == "PROBE2" or Type == "PROBE3" or Type == "PROBE4":
                        self.__mMeasInstrument.append(Cmp) # unnecessary copy
                        usedcmpnts[i] = False
        return usedcmpnts, usedInstrumentNodes, True

    def BuildCandidateCache(self):
        '''Crea la lista de candidatos y corto circuitos en cache (en un array de memoria temporal)
        Retorna Falso en caso de no encontrar ningun candidato especial.'''
        for i in range(0,len(self.__mIndexCircuit)):
            c = self.__mIndexCircuit[i]
            found = False
            candsize=len(self.__mCandidates)
            for j in range(0,candsize):
                if self.SpecialCompare(c, self.__mCandidates[j]):
                    self.__mCandCache[i].append(j)
                    found = True
            if not found:
                return False
        for i in range(0,len(self.__mCandidates)):
            c = self.__mCandidates[i]
            if c.GetType() == "SHORTCUT":
                self.__mShortcuts.append(i)
        return True

    def TierThree(self, circuit, candidates, symbols):
        ''' Resuelve la capa 3
        Parametros:
        circuit -- circuito
        candidates -- lista de candidatos
        symbols -- lista de simbolos
        '''
        self.__mIndexCircuit = circuit
        self.__mCandidates = candidates
        maxgroup = 0
        for i in range(0,len(self.__mCandidates)):
            c = self.__mCandidates[i]
            maxgroup = max(maxgroup, c.GetGroup())
        usage = [0]*(len(candidates) + maxgroup + 1)
        if not self.BuildCandidateCache():
            return False, usage
        # the actual solver
        # walk the list, sorted in connection order, and try to find a component matching and insertable
        return self.TierThreeSolveRecursive(0, usage, symbols)

    def TierThreeSolveRecursive(self, circuitidx, usage, symbols):
        ''' Resuleve recursivamente la capa 3
        Parametros:
        circuitidx -- El indice del circuito
        usage -- El vector de los usados
        symbols -- Vector de simbolos'''
        if circuitidx >= len(self.__mIndexCircuit):
            self.__mSolutionSymbols = symbols
            return True,usage # endcase
        current = self.__mIndexCircuit[circuitidx]
            # make a list of usable candidates, filtered from the candidate cache
        matching = []
        potential = self.__mCandCache[circuitidx]
        for i in range(0, len(potential)):
            if  not self.IsUsed(potential[i], usage):
                matching.append(potential[i])
        if not matching: # con esto chequeamos que esta vacio o no
            return False, usage
        circuitidx += 1
        boolean, usage =self.TryCandidateList(current, matching, circuitidx, usage, symbols, False)
        if boolean:
            return True,usage
        boolean, usage = self.TryCandidateList(current, matching, circuitidx, usage, symbols, True)
        if boolean:
            return True, usage
        return False, usage
    
    def TryCandidateList(self, current, matched, circuitidx, usage, symbols, withShortcuts):
        '''
        Parametros:
        current -- Componente actual
        matched -- Conjunto de candidatos encontrados
        circuitidx -- Indice del circuito
        usage -- Vector de usados
        symbols -- Vector de simbolos
        withShortCuts -- Indica si busca con cortocircuitos o no
        '''
        for i in range(0, len(matched)):
            isIprobe = False
            if current.GetType() == NamedNodes.DmmIProbe:
                isIprobe = True
            for turn in range(0, 2):
                symbolcopy = symbols
                out = []
                out, bolean = self.InsertIfValid(current, matched[i], turn, usage, symbolcopy, out, withShortcuts)
                if not bolean:
                    continue
                usage = self.UpdateUsageMap(usage, out, 1)
                boolRecursive, usage = self.TierThreeSolveRecursive(circuitidx, usage, symbolcopy)
                if not boolRecursive:
                    # no solution found, mark components as free again and continue
                    usage = self.UpdateUsageMap(usage, out, 0)
                    continue
                # we found a solution, trace back and add the components to the solution
                for solveit in out:
                    # dirty hack!  we should probably mark the briding shortcuts and make sure only the original is matched
                    if isIprobe and solveit == out[len(out)-1]: #saca el ultimo elemento del vector
                        iprobe = self.__mCandidates[solveit] # todo: validar
                        self.InsertIProbe(iprobe, turn, current.GetName())
                        self.__mSolution.append(iprobe)
                    else:
                        comp = self.__mCandidates[solveit] # todo: validar
                        if current.GetSpecial() != "":
                            comp.SetSpecial(current.GetSpecial())
                        self.__mSolution.append(comp)
                return True, usage
        return False, usage

    def SpecialCompare(self, c1, c2):
        ''' Dado dos componentes comprueba si son de tipo espacia Dmm o shortcut, en otro caso
        comprueba que sean iguales
        Parametros:
        c1 -- componente 1
        c2 -- componente 2'''
        if c1.GetType() == NamedNodes.DmmIProbe and c2.GetType() == "SHORTCUT":
            return True
        rv = c1.Equals(c2)
        return rv
    
    def InsertIfValid(self, circomp, netcomp_idx, turn, usage, symbolcopy, out, shortcut):
        '''Metodo que insterta en en un vector de usados en caso de ser valido
        Parametros:
        circomp -- Componente del circuito a validar
        netcomp_idx -- Indice del componente de candidatos a comparar
        turn -- Si se trata de un componente con caracteristicas especiales
        usage -- Vector de usados
        symbolcopy -- copia del simbolo
        out -- Vector de usados que se retorna
        shortcut -- Indica si se busca con cortocicuitos o no'''
        # we assume that the compared components have equal number of connections..
        netcomp = self.__mCandidates[netcomp_idx]
        if netcomp.CanTurn():
            # turning case
            node1 = circomp.GetConnections()[0]
            node2 = circomp.GetConnections()[1]
            netcons = netcomp.GetConnections()
            index1 = 0
            index2 = 1
            if turn: # turn no esta vacio?
                index1 = 1
                index2 = 0
            if not symbolcopy.ContainsSymbolOrEmpty(node1, netcons[index1]):
                # check if we can insert a shortcut to help us
                if shortcut:
                    symbolcopy, out, bolean = self.SearchShortcuts(symbolcopy, usage, node1, netcons[index1], out)
                    if not bolean:
                        return out, False
                else:
                    return out, False
            if not symbolcopy.ContainsSymbolOrEmpty(node2, netcons[index2]):
                # check if we can insert a shortcut to help us
                if shortcut:
                    symbolcopy, out, bolean = self.SearchShortcuts(symbolcopy, usage, node2, netcons[index2], out)
                    if not bolean:
                        return out, False
                else:
                    return out, False
            if symbolcopy.ContainsSymbol(node1, netcons[index2]):
                return out, False
            if symbolcopy.ContainsSymbol(node2, netcons[index1]):
                return out, False
            # these are the only ones modifying the symbol table
            if not symbolcopy.Insert(node1, netcons[index1]):
                return out, False
            if not symbolcopy.Insert(node2, netcons[index2]):
                return out, False
        else:
            # safeguard! we should really not be here.. but the algo is written that way.. for now..
            if (turn == 1):
                return out, False    
            numCon = len(circomp.GetConnections())
            for i in range(0,numCon):
                # NC* nodes are only allowed on multi legged components, ignore them as not existing
                netnode = netcomp.GetConnections()[i]
                if len(netnode) > 2 and netnode[0] == 'N' and netnode[1] == 'C':
                    continue # skip NC nodes
                symbol = circomp.GetConnections()[i]
                if not symbolcopy.ContainsSymbolOrEmpty(symbol, netcomp.GetConnections()[i]):
                    # check if we can insert a shortcut to help us
                    # XXX: Why am i not only doing this when shortcut search is on?
                    bolean, out, symbolcopy = self.SearchShortcuts(symbolcopy, usage, symbol, netcomp.GetConnections()[i], out)
                    if not bolean:
                        return out, False
                # Notice: if we failed on some iteration the symbolcopy will be invalid
                if not symbolcopy.Insert(symbol, netnode):
                    return out, False
        out.append(netcomp_idx)
        return out, True
    
    # This will modify the candidates and symbol table
    def SearchShortcuts(self, symbols2, usage, endnode, insertsymbol, solution):
        ''' Busca los cortocircuitos
        Parametros:
        symbols2 --
        usage --
        endnode --
        insertsymbol --
        solution --
        '''
        symbolscopy = None
        # find the shortest shortcut path between start and end
        # end can be many symbols. XXX: 
        # first make a list of all candidate shortcuts
        usableshorts = [] # En c++ reserva memoria nosotros en python no es necesario los vectores son dinamicos
        for i in range(0,len(self.__mShortcuts)):
            shrtidx = self.__mShortcuts[i]
            if not self.IsUsed(shrtidx, usage):
                cons = self.__mCandidates[shrtidx].GetConnections()
                if not symbols2.RefersSameNode(cons[0], cons[1]):
                    usableshorts.append(shrtidx)
        if not usableshorts: # chequeamos que no este vacia
            return symbols2, solution, False
        toVisit = collections.deque()
        # make the algorithm start at "startnode"
        toVisit.append(insertsymbol)
        rv = False
        tree = collections.OrderedDict() # dicionario ordenado, el dicionario normal de python es un poco caotico
        lastnode = ""
        while toVisit and not rv:
            lastnode = toVisit[0]
            if symbols2.ContainsSymbol(endnode, lastnode):
                rv = True
            bolean, tree, usableshorts, tovisit = self.SearchShortcutVisit(toVisit[0], toVisit, usableshorts, tree)
            toVisit.popleft()
        if rv:
            symbolscopy = symbols2 # don't copy until we really need it copied
            out = collections.deque()  # just a index array
            out, bolean = self.SearchShortcutBacktrace(tree, lastnode, insertsymbol, out)
            for it in out:
                comp = self.__mCandidates[it] # Esto puede que no funcione, en c++ le pasa it por puntero
                solution.append(it) # Esto pasa igual que el anterior
                if not symbolscopy.Insert(endnode, comp.GetConnections()[0]):
                    return symbolscopy, solution, False
                # Notice: if we failed on some iteration the symbolcopy will be invalid
                if not symbolscopy.Insert(endnode, comp.GetConnections()[1]):
                    return symbolscopy, solution, False
            symbols2 = symbolscopy
            return symbolscopy, solution, True
        return symbolscopy, solution, False            
    
    def SearchShortcutVisit(self, current, tovisit, edges, tree):
        ''' Busca los cortocircuitos que ya han sido visitados
        Parametros:
        current -- componente actual
        tovisit -- vector de componentes visitados
        edges -- vector con los cortociruitos
        tree -- Tabla has donde se almacenan las conexiones '''
        # find any shortcut leading from current
        # if we find a bridge, return
        # a partir de aqui lo he modificado un poco, ya que it en c++ es de tipo iterator y
        # estos son un tipo especial de puntero
        if len(edges) > 0:
            it = edges[0] 
            i = 0
            while i != len(edges):
                next = True
                cons = self.__mCandidates[it].GetConnections() 
                if cons[0] == current:
                    if not cons[1] in tree:
                        tree[cons[1]] = it
                        tovisit.append(cons[1])
                    next = False
                elif cons[1] == current:
                    if not cons[0] in tree:
                        tree[cons[0]] = it
                        tovisit.append(cons[0])
                    next = False
                if next:
                    i = i + 1
                    if i < len(edges):
                        it = edges[i]
                else:
                    it = edges.pop(i)                
                    if i < len(edges):
                        it = edges[i]

        return True, tree, edges, tovisit
    
    def SearchShortcutBacktrace(self, tree, lastnode, startnode, out):
        '''
        Parametros:
        tree --
        lastnode --
        startnode --
        out --'''
        # backtrace the found shortcut bridge
        current = lastnode
        done = False
        while not done:
            if not current in tree: # chequeamos si existe la clave
                done = True # salimos del dicionario, lo he añadido yo porque si no se quedaria en bucle infinito, al menos en python
            else:
                c_idx = tree[current]
                cons = self.__mCandidates[c_idx].GetConnections()
                if cons[0] == current:
                    out.append(c_idx)
                    current = cons[1]
                elif cons[1] == current:
                    out.append(c_idx)
                    current = cons[0]
                if current == startnode:
                    done = True
                    return out, True
        return out, False
    
    # utility functions
    def SetSymbol(self, node, symbol):
        '''Relaciona simbolo con nodo.
        Parametros:
        node -- nodo a insertar
        symbol -- simbolo a insertar'''
        self.__mSymbols.Insert(node,symbol)

    def GetSolution(self):
        '''Retorna la solucion encontrada'''
        return self.__mSolution
    
    def IsConnected(self, node):
        '''Comprueba que un nodo esta conectado o no.
        Parametros:
        nodo -- nodo a comprobar si esta conectado o no'''
        return self.__mSolutionSymbols.IsUsed(node)

    def GetFirstSymbol(self, sym):
        '''Retorna el primer nodo libre. Sino hay retorna NOSPARE
        Parametros:
        sym -- simbolo a asociar con el nodo '''
        return self.__mSolutionSymbols.GetFirstNodeOrSpare(sym)

    def InsertIProbe(self, component, turn, name):
        ''' Crea un componente de tipo DMM 
        Parametros:
        component -- El componentne a crear
        turn -- Si es especial o no
        name -- Nombre del componente'''
        component.SetType(NamedNodes.DmmIProbe)
        component.SetName(name)
        if turn:
            component.SetSpecial("1")
        else:
            component.SetSpecial("0")
        return component

    def AddInstrumentNodes(self, List):
        ''' Añade el intrument node en la lista de componentes
        Parametros:
        List -- Lista de componentnes'''
        for it in self.__mMeasInstrument:
            # The DMM has 2 connections that needs to be matched
            if it.GetType() == "DMM":
                sym1 = self.GetFirstSymbol(it.GetConnections()[0])
                sym2 = self.GetFirstSymbol(it.GetConnections()[1])
                if sym1 != "" and sym2 != "":
                    aComp = ListComponent(it.GetType(), it.GetName(), sym1, sym2)
                    List.append(aComp)
            else: # for now we assume that everything else just have one connection
                sym = self.GetFirstSymbol(it.GetConnections()[0])
                if sym != "":
                    aComp = ListComponent(it.GetType(), it.GetName(), sym)
                    List.append(aComp)
                
    def IsUsed(self, idx, usage):
        '''Retorna verdadero si el indice pasdo como parametro dentro de la
        lista de candidatos esta dentro de un grupo y además esta usado o esta usado
        Parametros:
        idx -- indice de los usados a buscar
        usage -- vector de usados'''
        if self.__mCandidates[idx].IsInGroup():
            return usage[len(usage) - self.__mCandidates[idx].GetGroup()] != 0
        else:
            return usage[idx] != 0
    
    def UpdateUsageMap(self, usage, update, state):
        ''''''
        for it in update:
            if self.__mCandidates[it].IsInGroup():
                 usage[len(usage) - self.__mCandidates[it].GetGroup()] = state
            else:
                usage[it] = state
        return usage

    def DumpCandidateList(self, List):
        '''Imprime la lista de candidatos.
        Parametros:
        List -- Lista de candidatos'''
        out = "-CANDIDATE DUMP-" + "\n"
        for it in List:
            out = out + "Dump: " + it.Dump() + "\n"
        return out
    
    def DumpIndicesList(self, List, circuit):
        '''Imprime a cadena la lista de indices
        Parametros;
        List -- Lista de indices
        circuit -- Circuito'''
        out = "-INDICES DUMP-" + "\n"
        for it in List:
            out = out + "Dump: " + circuit[it].Dump() + "\n"
        return out