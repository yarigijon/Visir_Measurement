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

from circuitsolver.listparser import *
from circuitsolver.compdefreader import ComponentDefinitionRegistry
from eqcom.eqcom import EQCom

class Circuit (object):
    def __init__(self, ComponentsDefinitions=None):
        ''' Almacenamos los componentes disponibles en el EQ server en ComponentList y self.Error = True
        si el mensaje de respuesta da un error self.Error = False y se almacena el error en self.ComponentList'''
        if ComponentsDefinitions:
            EQServer = EQCom()
            EQServer.SendComand("system","000011\ndata\n41\t4\n")
            Response = EQServer.GetResponse("system")
            self.Error, self.ComponentList = self.ParseGetComponentListResponse(Response, ComponentsDefinitions)
        else:
            ComponentsDefinitionsFromRegistry = ComponentDefinitionRegistry()
            self.ComponentList = ComponentsDefinitionsFromRegistry.GetComponentList()

        
    def ParseGetComponentListResponse(self, Response, ComponentsDefinitions):
        if len(Response)-6 == int(Response[:6]) and Response.find("data\n41 4\t") != -1:
            Init = Response.find("\t")+1
            End = Response.find("?")
            parser = ListParser(ComponentsDefinitions)
            Component = Response[Init:End]
            List = Response[End+1:]
            Buffer = Component + "\n"
            while List.find("?") != -1:
                End = List.find("?")
                Component = List[:End]
                Buffer += Component + "\n"
                List = List[End+1:]
            End = List.find("\n")
            Component = List[:End]
            Buffer += Component + "\n"
            parser.Parse(Buffer)
            ComponentList = parser.GetList()
            return False, ComponentList
        else:
            if len(Response)-7 != int(Response[:6]):
                Msg = "Response length incorrect"
            else:
                Msg = Response[Response.find("error\n") + 6:]
            return True, Msg
        
    def InstrumentBuild(self, Solution):
        Out = ""
        for Item in Solution:
            if Item.GetType() == "PROBE1" or Item.GetType() == "PROBE2":
                if Out == "":
                    Out += self.OscilloscopeBuild(Item)
                else:
                    Out += "?" + self.OscilloscopeBuild(Item)
            elif Item.GetType() == "DMM" or Item.GetType() == "IPROBE":
                if Out == "":
                    Out += self.MultimeterBuild(Item)
                else:
                    Out += "?" + self.MultimeterBuild(Item)
        if Out == "":
            return Out
        else:
            return "41\t6 " + Out  + "\n"

    def OscilloscopeBuild(self, Item):
        if Item.GetType() == "PROBE1":
            Out = "OSC " + Item.GetName() + " 1 " + Item.GetConnections()[0]
        elif Item.GetType() == "PROBE2":
            Out = "OSC " + Item.GetName() + " 2 " + Item.GetConnections()[0]
        return Out

    def MultimeterBuild(self, Item):
        Out = "DMM " + Item.GetName() + " "
        if Item.GetType() == "DMM":
            Out += "V "
        elif Item.GetType() == "IPROBE":
            Out += "I "
        Out += Item.GetConnections()[0] + " " + Item.GetConnections()[1]
        return Out

    def CircuitBuild(self, Solution):
        '''
            Metodo que crea los comandos para EQ server.

        Paramnetros:
            Solution [listcomponent] lista de nodos y componentes con la solucion encontrada
            ComponentList [listcomponent] lista de nodos y componentes disponibles en el EQ server
        '''
        Out = ""
        Nodes = self.RemoveTypes("DMM", Solution)
        Nodes = self.RemoveTypes("IPROBE", Nodes)
        Nodes = self.RemoveTypes("PROBE1", Nodes)
        Nodes = self.RemoveTypes("PROBE2", Nodes)
        Nodes = self.RemoveTypes("XSWITCHCLOSE", Nodes)
        Nodes = self.ReplaceType("XSWITCHOPEN", "SHORTCUT", Nodes)
        MatchedNodes, Boolean = self.MatchIndex(Nodes, self.ComponentList)
        if not MatchedNodes: # Si esta vacio retornamos True, pero el vector lo pasamos vacio
            Out = []
            return True, Out
        Out = "41\t" + "3 "
        First = True
        for It in MatchedNodes:
            if not First:
                Out += "?"
            else:
                First = False
            Out += self.ComponentList[It[0]].GetName()
        return Out + "\n"
                       
    def ReplaceType(self, OriginalType, NewType, Nodes):
        for i in range(0, len(Nodes)):
            if OriginalType == Nodes[i].GetType():
                Nodes[i].SetType(NewType)
        return Nodes

    def RemoveTypes(self, Type, Nodes):
        TempNodes = []
        for Item in Nodes:
            if Item.GetType() != Type:
                TempNodes.append(Item)
        return TempNodes

    def MatchIndex(self, Subset, Superset):
        '''Retorna un vector de pares que contiene el indice del superconjunto y
        el indice del subconjunto donde ambos nodos coincidente
        Ademas retornara verdadero en caso de encontrar el subconjunto dentro del superconjunto
        falso en el primer momento que un elemento del subconjunto no este dentro del superconjunto

        Parametros:
        Subset -- subconjunto de nodos a buscar
        Superset -- lista de componentes
        '''
        Out = []
        Used = [0]*len(Superset) #inicializamos used con tantos 0 como tamano tiene superset
        for Subi in range(0,len(Subset)):
            Matched = False
            for Superi in range(0,len(Superset)):
                if Matched:
                    break
                if Used[Superi]==0 and Subset[Subi].EqualsWithConnection(Superset[Superi]):
                    Matched = True
                    Used[Superi] = 1
                    Pair = (Superi, Subi) #Diccionario a retornar con par de Subset y Superset que coinciden
                    Out.append(Pair)
            if not(Matched):
                Pair = (-1, Subi)
                Out.append(Pair)
        NotMached = False
        for Item in Out:
            if Item[0]==-1:
                NotMached = True
        if NotMached:
            return Out, False
        else:
            return Out, True

