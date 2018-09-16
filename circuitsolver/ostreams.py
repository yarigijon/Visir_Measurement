# coding=utf-8
__all__ = ["endl", "OStream", "IOstreamsManipulator"] # esto es lo que se importa al poner=> from ostreams import *

class IOstreamsManipulator(object):
    '''Objeto al que le puedes pasar cualquier funcion para ejecutar'''
    def __init__(self, function=None):
        '''Constructor que le asigna la funcion que queremos que haga en el do'''
        self.function = function
    def do(self, output):
        '''Ejecuta la funcion pasada como parametro en el constructor
        Parametros:
        output -- parametro de entrada.'''
        self.function(output)

def do_endl_streams(stream):
    '''Añade al fichero el salto de linea y libera los buffers'''
    stream.output.write('\n')
    stream.output.flush()

endl = IOstreamsManipulator(do_endl_streams)

class OStream(object):
    '''Clase que crea un objeto que va escribiendo por la salida
    definida en el contructor (estandar, fichero...)'''
    def __init__(self, output=None):
        '''Constructor que inicializa la clase OStream, inicializa la
        salida (si es vacio es la estandar) y el formato (tipo string)'''
        import sys
        if output is None:
            output = sys.stdout
        self.output = output
        self.format = '%s'
            
    def __lshift__(self, thing):
        '''Python will call this function when you use << with left operator being OStream
        '''
        if isinstance(thing, IOstreamsManipulator):
            thing.do(self)
        else:
            self.output.write(self.format % thing)
            self.output.flush()
            self.format = '%s'
        return self