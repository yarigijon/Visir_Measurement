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

import string

'''Funciones basicas para utilizar con cadenas'''
__all__ = ['ToString', 'ToStringScientific', 'ToDouble',
           'ToStringbitfield', 'find_first_not_of',
           'find_first_of', 'find_last_of', 'find_last_not_of',
           'Token', 'RemoveToken', 'Tokenize', 'ToLower', 'ToUpper',
           'GetLine', 'CleanWhitespaces', 'ToCRLF', 'AddWhitespace', 'npos']

# convierte entero o float a string


def ToString(x):
    '''Convierte un entero a string

    Parametros:
    x -- el entero a convertir
    '''
    return str(x)

# convierte float en notacion cientifica, en python es igual al
# anterior (pero por compatibilidad con codigo c++ se crea)


def ToStringScientific(x):
    '''Convierte un float en notacion cientifica

    Parametro:
    x -- flotante a convertir
    '''
    return str(x)

# convierte string a float


def ToDouble(instring):
    '''Convierte una variable de tipo cadena en double

    Parametros:
    instring -- cadena de entrada
    '''
    return float(instring)

# convierte a string de 1 y 0 un valor


def ToStringbitfield(val, Len):
    '''Convierte a binario un valor
    retorna el string de 1 y 0s

    Parametros:
    val -- valor a transformar
    Len -- tamano
    '''
    # assume MSB -> LSB
    tempstring = ""
    testbit = 1 << (Len - 1)
    for i in range(0, Len):
        if val & testbit:
            tempstring = tempstring + "1"
        else:
            tempstring = tempstring + "0"
        testbit = testbit >> 1
    return tempstring


def npos():
    return -1

# funcion creada por mi para compatibilidad con c++


def find_first_not_of(*arg):
    '''Busca el primero que no es igual a alguno de los caracteres de chars
        empieza a buscar a partir de pos

        Parametros:
        arg -- vector que puede tomar diferentes tamanos, donde el primer
        parametro es el caracter, el segundo los caracteres a buscar y el
        tercero opcional el index donde empezar a buscar. Por defecto es 0.
        '''
    if len(arg) == 3:
        string = arg[0]
        chars = arg[1]
        pos = arg[2]
    else:
        string = arg[0]
        chars = arg[1]
        pos = 0
    for i in range(pos, len(string)):
        result = True
        for it in chars:
            result = result and (string[i] != it)
        if result:
            return i
    return npos()

# funcion creada por mi para compatibilidad con c++


def find_first_of(*arg):
    '''Busca el primero que es igual a alguno de los caracteres de chars
       empieza a buscar a partir de una posicion dada.

        Parametros:
        arg -- vector que puede tomar diferentes tamanos, donde el
        primer parametro es el caracter, el segundo los caracteres a buscar
        y el tercero opcional el index donde empezar a buscar. Por defecto
        es 0.
    '''
    if len(arg) == 3:
        string = arg[0]
        chars = arg[1]
        pos = arg[2]
    else:
        string = arg[0]
        chars = arg[1]
        pos = 0
    for i in range(pos, len(string)):
        result = False
        for it in chars:
            result = result or (string[i] == it)
        if result:
            return i
    return npos()


def find_last_not_of(*arg):
    '''Busca el primero que no es igual a alguno de los caracteres de chars
       empieza a buscar a partir de una posicion dada.

       Parametros:
       arg -- vector que puede tomar diferentes tamanos, donde el primer
       parametro es el caracter, el segundo los caracteres a buscar y
       el tercero opcional el index donde empezar a buscar.
       Por defecto es 0.
    '''
    if len(arg) == 3:
        string = arg[0]
        chars = arg[1]
        pos = arg[2]
    else:
        string = arg[0]
        chars = arg[1]
        pos = 0
    # Descuenta inversa desde longitud del array - 1 y siempre que sea mayor
    # de -1 (es decir 0)
    for i in range(len(string) - 1, -1, -1):
        result = True
        for it in chars:
            result = result and (string[i] != it)
        if result:
            return i
    return npos()


def find_last_of(*arg):
    '''Busca en la cadena el ultimo caracter que coincida con cualquiera
        de los caracteres especificados en sus argumentos.

        Cuando se especifica el ultimo parametro de arg, la busqueda
        solo incluye caracteres en o antes de la posicion pos, ignorando
        cualquier posible ocurrencia despues de pos.

        Parametros:
        arg -- vector que puede tomar diferentes tamanos, donde el primer
        parametro es el caracter, el segundo los caracteres a buscar y
        el tercero opcional el index donde empezar a buscar.
        Por defecto es 0.
    '''
    if len(arg) == 3:
        string = arg[0]
        chars = arg[1]
        pos = arg[2]
    else:
        string = arg[0]
        chars = arg[1]
        pos = 0
    # Descuenta inversa desde longitud del array - 1 y siempre que sea mayor
    # de -1 (es decir 0)
    for i in range(len(string) - 1, -1, -1):
        result = False
        for it in chars:
            result = result or (string[i] != it)
        if result:
            return i
    return npos()

# esta funcion existe con 3 o 2 parametros, con 2 toma por defecto string "/t "


def Token(*arg):
    '''Devuelve un token.

    Parametros:
    arg -- es un vector de tamano variable que contiene al menos la cadena
    de entrada, el numero de tokens y opcionalmente una variable
    booleana que indican los separadores, por defecto tabulador y
    espacio en blanco.
    '''
    if len(arg) == 3:
        instring = arg[0]
        tokennum = arg[1]
        tokenchars = arg[2]
    else:
        instring = arg[0]
        tokennum = arg[1]
        tokenchars = "\t "
    pos = 0
    for i in range(
            0,
            tokennum +
            1):  # Esto range hace <tokennum por eso se suma 1
        if i != 0:  # eat whitespaces and tabs
            pos = find_first_not_of(instring, tokenchars, pos)
        if pos == npos():
            return ""
        # get token!
        endpos = find_first_of(instring, tokenchars, pos)
        # return the whole string.. but all tokens after should be ""
        if endpos == npos():
            outstring = instring[pos:]
        else:
            outstring = instring[pos:endpos]
        pos = endpos
    return outstring

# removes everything from start to token tokennum


def RemoveToken(*arg):
    '''Elimina todo desde el comienzo hasta tokenum

    Parametros:
    arg -- vector de tamano variable que contiene la cadena de
    entrada el numero de tokens y como opcional el separador,
    por defecto, el tabulador y el espacio.
    '''
    if len(arg) == 3:
        instring = arg[0]
        tokennum = arg[1]
        tokenchars = arg[2]
    else:
        instring = arg[0]
        tokennum = arg[1]
        tokenchars = "\t "
    pos = 0
    for i in range(0, tokennum + 1):
        # eat whitespaces and tabs
        pos = find_first_not_of(instring, tokenchars, pos)
        # get token!
        endpos = find_first_of(instring, tokenchars, pos)
        # strip trailing tokenchars
        endpos = find_first_not_of(instring, tokenchars, endpos)
        if endpos != npos():
            outstring = instring[endpos:]
        else:
            outstring = ""
        pos = endpos
    return outstring

# TODO: Hay un bug, si pones dos espacios en blanco o espacio
# en blanco y tabulador tal y como esta hecha esta funcion
# te daria el espacio en blanco/tabulador de mas como token


def Tokenize(*arg):
    '''
    Separa una cadena por los separadores pasado como parametros.
    Devuelve un array con la cadena separada.

    Parametros:
    arg -- es un vector de tamanto variable que contiene al menos la cadena
    de entrada, el vector de salida los separadore y opcionalmente una variable
    booleana que indica si hay que borrar los separadores duplicados o no.
    '''
    if len(arg) == 4:
        inString = arg[0]
        outContainer = arg[1]
        separators = arg[2]
        removeDuplicateSeparators = [3]
    else:
        inString = arg[0]
        outContainer = arg[1]
        separators = arg[2]
        removeDuplicateSeparators = False
    if inString == "":
        return
    curPos = 0
    while curPos != npos():
        if removeDuplicateSeparators:
            curPos = find_first_not_of(inString, separators, curPos)
        endPos = find_first_not_of(inString, separators, curPos)
        endPos = find_first_of(inString, separators, endPos)
        if endPos == npos():
            if curPos != npos():
                outContainer.append(inString[curPos:])
            curPos = npos()
        else:
            outContainer.append(inString[curPos:endPos])
            curPos = endPos + 1
    return outContainer


def ToLower(instring):
    '''Convierte a minisculas.

    parametros:
    instring -- cadena de entrada
    '''
    return instring.lower()


def ToUpper(instring):
    '''Convierte a mayuscula.

    parametros:
    instring -- cadena de entrada
    '''
    return instring.upper()


def GetLine(instring, outstring):
    '''
    Obtiene la primera linea de instring y la devuelve en outstring, ademas
    elimina de instring esa linea.

    Parametros:
    instring -- cadena de entrada
    outstring -- cadena de salida que contiene la primera linea que
    encuentra en la cadena de entrada.
    '''
    if instring == "":
        # revisar si realmente hay que retornar instring
        return instring, "", False
    pos = find_first_of(instring, "\n\r")
    if (pos != npos()):
        outstring = instring[0: pos]
        endpos = find_first_not_of(instring, "\n\r", pos)
        if (endpos == npos()):
            instring = ""
        else:
            instring = instring[endpos:]
    else:
        outstring = instring
        instring = ""
    return instring, outstring, True


def CleanWhitespaces(instring):
    ''' Elimina los espacios en blanco del final del string.
    Retorna el string sin espcios en blanco.

    Parametros:
    instring -- Cadena de entrada donde eliminar los espacios en blanco.
    '''
    first = find_first_not_of(instring, " \t")
    last = find_last_not_of(instring, " \t")
    if first == npos():
        return ""
    if last == npos():
        return ""
    return instring[first:last - first + 1]


def ToCRLF(instring):
    '''Anade \r a cada salto de linea. y Devuelve el
    string modificado.

    Parametros:
    instring -- cadena a modificar.
    '''
    outstring = ""
    for i in instring:
        if i == '\n':
            outstring = outstring + "\r\n"
        else:
            outstring = outstring + i
    return outstring


def AddWhitespace(instring, length):
    '''Anade tantos espacions en blanco a la cadena como indica length

    parametros:
    instring -- cadena a rellenar con espacion en blanco
    lenght -- numero de espacios en blanco a anadir, en realidad
    es lenght menos el tamano de la cadena lo que se rellenara
    de espacios en blanco.
    '''
    outstring = instring
    while len(outstring) < length:
        outstring = outstring + " "
    return outstring
