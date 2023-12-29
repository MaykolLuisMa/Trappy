import socket
import os
from chronometer import *
from packet import *
from typing import Tuple

class Conn:    
    def __init__(self, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        self.source_host = None
        self.source_port = None
        self.dest_host = None
        self.dest_port = None
        self.isClosed = False

        self.socket = sock

    def close(self):
        #Aqui reiniciaremos todos los atributos
        self.socket.close()
        self.host = None
        self.port = None
        self.isClosed = True
    
    def bind(self, host = None, port = None):
        if (host == None):
            host = ''
        self.host = host
        if (port == None):
            port = 0 #Al hacer bind al puerto 0, el OS automaticamente nos encuentra un puerto libre
        self.socket.bind(self.host, port)
        self.port = self.socket.getsockname()[1] #Averiguando que puerto fue asignado
    
    #Devuelve una tupla con el paquete recibido y el address de donde vino
    def recv(self, timeout=0.5) -> Tuple[Packet, str] | None:
        pass

    #Devuelve la cantidad de bits enviados
    def send(self, data) -> int:
        pass


class ConnException(Exception):
    pass