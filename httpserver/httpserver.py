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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from server import Bottle, template, redirect, request, response, template, static_file, route
from authenticator.client import Client
from transation import Transation
from xmlserver.xmlparser import XMLParser
import datetime
import os

web = Bottle()
CurrentPath = os.getcwd()
PathHttpTemplates = os.path.join(CurrentPath, "httpserver")
PathHttpTemplates = os.path.join(PathHttpTemplates, "www")
VisirPath = os.path.join(PathHttpTemplates, "visir")

class HttpServer(object):
    def __init__(self, host, port, Quiet):
        self.host = host
        self.port = port
        self.Quiet = Quiet
        self.ClientIP = ""
        Now = str(datetime.datetime.now())
        print "[" + Now + "] Started HTTP server on port " + str(port)
        CurrentPath = os.getcwd()
        self.PathHttpTemplates = os.path.join(CurrentPath, "httpserver")
        self.PathHttpTemplates = os.path.join(self.PathHttpTemplates, "www")
        self.VisirPath = os.path.join(self.PathHttpTemplates, "visir")
        self.VisirInstrumentsPath = os.path.join(self.VisirPath, "instruments")

    def Init(self):
        ''' Inicializa el servidor http'''
        web.run(host=self.host, port=self.port, quiet=True)
    
    def Close(self):
        ''' Para la ejecucion del servidor http''' 
        self.app.close()

@web.route('/')
def Index():
    ClientInfo()
    return static_file("index.html" , root='httpserver/www')
	
@web.route('/aboutus')
def Index():
    ClientInfo()
    return static_file("/static/aboutus.html" , root='httpserver/www')
	
@web.route('/login')
def Index():
    ClientInfo()
    return static_file("/static/login.html" , root='httpserver/www')

@web.route('/visir')
def Visir():
    ClientInfo()
    return static_file("visir.html" , root=VisirPath)
	
@web.get('<filename:re:.*\.eot>')
def javacripts(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.woff>')
def javacripts(filename):
    return static_file(filename, root='httpserver/www')
	
@web.get('<filename:re:.*\.ttf>')
def javacripts(filename):
    return static_file(filename, root='httpserver/www')
	
@web.get('<filename:re:.*\.svg>')
def javacripts(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.js>')
def javacripts(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.json>')
def image(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.png>')
def image(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.ttf>')
def image(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.xml>')
def image(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.tpl>')
def image(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.svg>')
def image(filename):
    return static_file(filename, root='httpserver/www')

@web.get('<filename:re:.*\.jpg>')
def image(filename):
    return static_file(filename, root='httpserver/www')

@web.post('/measureserver')
def MeasurementHandler():
    ClientInfo()
    XMLRequest = request.body.read()
    TransationHandler = Transation()
    XMLResponse = TransationHandler.ProcessRequest(XMLRequest)
    print  "\t\033[34mHTTP Response:\033[0m POST /measureserver" 
    return XMLResponse

def ClientInfo():
    Method = str(request.environ['bottle.request'])
    Method = Method[Method.find(":")+1:Method.find("http:")]
    ClientIP = request.environ.get('REMOTE_ADDR')
    PathInfo = request.environ['PATH_INFO']
    Now = str(datetime.datetime.now())
    print "[" + Now + "] HTTP connection from: " + ClientIP
    print "\t\033[34mHTTP request:\033[0m " + Method + PathInfo 
