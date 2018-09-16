# coding=utf-8
from listcomponent import ListComponent
from basic_exception import BasicException
from collections import OrderedDict
from stringop import *


class ComponentTypeDefinition(object):
    ''' Definicion de la clase component type definition, donde se definen las variables
    que componen la clase así como su constructor y los metodos necesarios para acceder y
    retornar todas esas variables.
    '''

    def __init__(self, *arg):
        '''Constructor por defecto. Ó el construnctor por parametros
        con los 5 valores necesarios para inicializar el components type'''
        self.__mType = None
        self.__mNumCons = None
        self.__mCanTurn = None
        self.__mIgnoreValue = None
        self.__mHasSpecialValue = None
        if len(arg)==5:
            self.__mType = arg[0]
            self. __mNumCons = arg[1]
            self.__mCanTurn	= arg[2]
            self.__mIgnoreValue	= arg[3]
            self.__mHasSpecialValue	= arg[4]
        else:
            self.__mType = "Undefined"
            self.__mNumCons = 0
            self.__mCanTurn = False
            self.__mIgnoreValue = False
            self.__mHasSpecialValue = False

    def Type(self):
        '''Retorna el tipo type de la clase component type.
        '''
        return self.__mType
    
    def NumConnections(self):
        ''''Retorna el numero de conexiones de la clase component type'''
        return self.__mNumCons
    
    def IgnoreValue(self):
        '''Retorna un boleano indicando si hay que ignora el valor o no'''
        return self.__mIgnoreValue

    def HasSpecialValue(self):
        '''Retorna un booleano indicando si la clase tiene valores o especiales
        o no.'''
        return self.__mHasSpecialValue 

class ListParser(object):
    '''
    Parsea una lista de componentes.
    '''
    def __init__(self, definitions):
        '''Construcctor, al inicio se crea un dicionatio con clave los diferentes
        tipos de componentes y valor su definicion completa, incluido su tipo'''
        self.__mComponentList=[]
        self.__mCompDefMap = OrderedDict()
        for it in definitions:
            self.__mCompDefMap[it.Type()]=it #Añadimos al dicionario clave it.Type y valor it

    def CreateComponent(self, instring):
        '''
        Crea un componente a partir de una cadena que contiene la definicion.
        Parametros:
        instring -- Cadena de texto a procesar.
        '''
        # obtenermos la primera palabra de la linea que es el tipo_nombre
        type_name = Token(instring, 0)
        # le eliminamos la primera palabra y guardamos el resultado en restofstring
        restofstring = RemoveToken(instring, 0)
        # buscamos el tipo, separando por \t o _ el primero que encuentre
        Type = Token(type_name, 0, "\t _")
        # eliminamos la primera parte y nos quedamos el resto en name
        name = RemoveToken(type_name, 0, "_")
        groupID = 0
        atPos = find_first_of(name, "@")
        if atPos != npos(): # ¿existe posicion con @ en el nombre? si existe entra
            groupID = int (name[atPos+1:]) # carga todo lo que hay despues de la @ convertido a int
            name = name[0:atPos-1] # carga en name todo la cadena hasta la @ no incluida
            if (groupID > 20):
                raise BasicException("unexpected group id in maxlist") # lanzamos una exception personalizada
        pType = self.GetTypeDefinition(Type)
        if (not pType):
            return None
        pComponent = ListComponent(Type, name)
        for i in range(0,pType.NumConnections()):
            con = Token(restofstring, 0)
            if con == "":
                return None; # fail
            restofstring = RemoveToken(restofstring, 0)
            pComponent.AddConnection(con)
        if not pType.IgnoreValue():
            if restofstring != "":
                value = Token(restofstring, 0)
                pComponent.SetValue(value)
                restofstring = RemoveToken(restofstring, 0)
        if pType.HasSpecialValue():
            pComponent.SetSpecial(restofstring)
        pComponent.SetGroup(groupID)
        return pComponent

    def IsComment(self, instring):
        '''
        Indica si la linea procesada es un comentario o no.
        Retorna True en caso de ser un comentario, false en otro caso.

        Parametros:
        instring -- cadena de texto, que sera chequeada para saber si es 
        un comentario o no.
        '''
        if instring == "":
            return True
        pos = find_first_not_of(instring, " \t")
        if pos != npos():
            if (instring[pos] == '#') or (instring[pos] == '*'):
                 return True
        else:
            return  # solo hay una linea en blanco en la linea
        return False

    def Parse(self, aList):
        '''Parsea de una cadena que contiene la lista de parametros
        a un array que contiene los componentes definidos en la lista.
        Parametros:
        aList -- Lista de lineas a procesar.
        '''
        self.__mComponentList = [] #nuke all old nodes
        line = "" #declaramos line como string vacio para poder pasarlo a la funcion siguiente
        aList, line, bolean = GetLine(aList, line) # GetLine en util/stringop
        while (bolean):
            pos = find_first_of(line, "*#")
            if (pos != npos()):
                line = line[0:pos-1] #nos quedamos con el trozo de 0 a pos
            if self.IsComment(line):
                # chequeamos que no es una linea de comentario o esta en blanco
                aList, line, bolean = GetLine(aList, line)
                continue  # si es una linea de comentario, continuamos con la siguiente
            line = ToUpper(line) #convertimos a mayusculas
            pComp = self.CreateComponent(line) # Creamos componete a partir de la linea
            if not pComp: # chequea si esta vacio
                del pComp # el componente esta vacio podemos destruirlo
                return False
            else:
                self.__mComponentList.append(pComp)
                del pComp # nosotros hemos compiado el contenido podemos destruirlo                
            aList, line, bolean = GetLine(aList, line) #tiene que hacerse al final de while
        return True

    def GetList(self):
        '''Retorna la lista de componentes parseada'''
        return self.__mComponentList

    def ParseFile (self, filename):
        '''Parsea un archivo.
        Parametros:
        filename -- Nombre del archivo a parsear'''
        stringBuffer =""
        try :
            file = open(filename, "r") # abrimos el archivo en solo lectura
            #with open(filename, 'r') as file:
            for line in file:
                stringBuffer = stringBuffer + line + "\n"
            file.close()
        except IOError:
            return False
        # Leemos el fichero linea a linea        
        return self.Parse(stringBuffer) # retornamos True si consigue parsear buffer

    def GetTypeDefinition(self, Type):
        '''
        Retorna el componente asociado al tipo.
        Parametros:
        type -- el tipo a buscar dentro del diccionario.
        '''
        try:
            # retornamos valor
            return self.__mCompDefMap[Type]
        except:
            return None # en caso de no existir retornamos vacio
