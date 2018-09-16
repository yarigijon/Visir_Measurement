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

import datetime
import time
import os
import string
from socket import *
from instruments import Circuit
from circuitsolver.compdefreader import *
from circuitsolver.listparser import *
from httpserver.httpserver import HttpServer
from eqcom.eqcom import EQCom
from authenticator.authenticator import Authentication
from authenticator.session import SessionRegistry
from circuitsolver.maxfilesregistry import MaxFilesRegistry
from authenticator.client import Client, ClientRegistry #Anadido para pruebas eliminar client solo

def main():
    #########################################################################################
    # Configuracion Inicial, Valores por defecto
    ##########################################################################################
    EQ = "localhost"
    EQPort = 5001 #Visir
    NumMaxSessions = 30
    SessionTimeOut = 3600
    HttpPort = 80
    AllowKeepAlive = True
    ByPassAuth = True
    ###########################################################################################
    Version = "00.00.02 Beta"
    Now = str(datetime.datetime.now())
    print "******************************************************"
    print "*** Visir Measurement Server Version " + Version + " ***"
    print "******************************************************"
    print "[" + Now + "] Starting server"
    CurrentPath = os.getcwd()
    ConfigPath = os.path.join(CurrentPath, "conf")
    ConfigFile = os.path.join(ConfigPath, "measureserver.conf")
    Now = str(datetime.datetime.now())
    print "[" + Now + "] Read Config File"
    File = None
    try:
        File = open(ConfigFile,"r")
    except:
        # chequeamos que realmente se ha abierto el fichero si no parametros por defecto y advertencia
        print "\t\033[35mWARNING:\033[0m Config File not found, default values are used"
    if File:
        Line = File.readline() #leemos la primera linea
        while Line:
            if Line[0] != "#": #Linea comentada, se ignora
                End = Line.find(" ")
                if End != -1:
                    Comand = Line[:End]
                    Value = Line[End+1:Line.find("\n")]
                    if Comand == "EQ":
                        EQ = Value
                    elif Comand == "EQPort":
                        EQPort = int(Value)
                    elif Comand == "ByPassAuth":
                        ByPassAuth = bool(Value)
                    elif Comand == "NumMaxSessions":
                        NumMaxSessions = int(Value)
                    elif Comand == "SessionTimeOut":
                        SessionTimeOut = int(Value)
                    elif Comand == "AllowKeepAlive":
                        AllowKeepAlive = bool(Value)
                    elif Comand == "HttpPort":
                        HttpPort = int(Value) 
            Line = File.readline()
    FileComponentsType =  os.path.join(ConfigPath, "component.types")
    componentReader = ComponentDefinitionReader()
    componentReader.ReadFile(FileComponentsType)
    ComponentsDefinitions = componentReader.GetDefinitions()
    ComponentDefinitionRegister = ComponentDefinitionRegistry()
    ComponentDefinitionRegister.Register()
    ComponentDefinitionRegister.AddComponentDefinition(ComponentsDefinitions)
    Now = str(datetime.datetime.now())
    print "[" + Now + "] Reading maxlist config"
    FileMaxList = os.path.join(ConfigPath, "maxlist.conf")
    MaxFilesComponents = []
    MaxFilesName = []
    MaxfilesRegister = MaxFilesRegistry()
    MaxfilesRegister.Register()
    File = open(FileMaxList,"r") # Si no localiza archivo con maxlist error y no merece la pena crear excepcion
    Line = File.readline() #leemos la primera linea
    Parser = ListParser(ComponentsDefinitions)
    while Line:
        if Line[0] != "#": #Linea comentada, se ignora
            Num = Line.find(".max")
            if Line[0] == "/" or Line[0] == "\\":
                Line = Line[1:Num] + ".max"
            else:
                Line = Line[0:Num] + ".max"
            if os.sep == "\\":
                Line = string.replace(Line, "/", "\\")
            else:
                Line = string.replace(Line, "\\", "/")
            Now = str(datetime.datetime.now())
            print "[" + Now + "] Reading maxlist: " + Line
            #Line = os.path.normpath(Line) #Solo funcionaba en algunos OS
            MaxFile = os.path.join(ConfigPath, Line)
            Parser.ParseFile(MaxFile)
            MaxFilesName.append(Line)
            MaxFilesComponents.append(Parser.GetList())
            MaxfilesRegister.AddMaxFile(Parser.GetList())
        Line = File.readline()
    Now = str(datetime.datetime.now())
    print "[" + Now + "] Loading module: EQCOM"
    EQServer = EQCom()
    Now = str(datetime.datetime.now())
    print "[" + Now + "] Registering EQCOM Module"
    EQServer.Register(EQ,EQPort)
    Now = str(datetime.datetime.now())
    print "[" + Now + "] Sending component list request to equipment server"
    EQCircuit = Circuit(ComponentsDefinitions)
    if EQCircuit.Error:
        print "\033[31mError:\033[0m " + str(EQCircuit.ComponentList)
    else:
        for It in range(0,len(MaxFilesComponents)):
            Value, Boolean = EQCircuit.MatchIndex(MaxFilesComponents[It], EQCircuit.ComponentList)
            if not Boolean:
                print "\033[35mWARNING:\033[0m Maxlist " + MaxFilesName[It] + " is not a subset of the componentlist"
                for Item in Value:
                    if Item[0]==-1:
                        MaxFileFail = MaxFilesComponents[It]
                        print "\t - Failed on " + MaxFileFail[Item[-1]].Dump()
                print "\033[31mError:\033[0m The returned componentlist is not a superset of the used maxlists"
        ComponentDefinitionRegister.AddComponentList(EQCircuit.ComponentList)
        SessionControl = SessionRegistry()
        SessionControl.Register(NumMaxSessions,SessionTimeOut)
        Now = str(datetime.datetime.now())
        print "[" + Now + "] Registering Authentication Module"
        VisirAuthentication = Authentication()
        VisirAuthentication.Register(SessionControl,AllowKeepAlive, ByPassAuth)
        #VisirAuthentication.RegisterAuthenticator() #Aqui se registrarian los diferentes modos de autentificar
        VisirAuthentication.Init() # Inicializamos los diferentes metodos de autentificacion si ByPassAuth se lo salta
        ClientList = ClientRegistry()
        ClientList.Register()
        #****************************************************************************
        # Eliminar la funcion siguiente solo creada en primera version para pruebas
        #****************************************************************************
        TestClient = Client()
        ClientList.AddClient(TestClient)
        Now = str(datetime.datetime.now())
        print "[" + Now + "] Initialization complete, staring to listen for incoming connections"
        WebServer = HttpServer('0.0.0.0',HttpPort, True)
        WebServer.Init()
        
        
if __name__ == "__main__":
    main()