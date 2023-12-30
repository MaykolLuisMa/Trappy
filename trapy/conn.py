import socket
import os
from chronometer import *
from packet import *
from typing import Tuple

class Conn:    
    def __init__(self, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        self.max_data_size = 512
        self.bufsize = 20 + 20 + self.max_data_size
        self.source_host = None
        self.source_port = None
        self.dest_host = None
        self.dest_port = None
        self.isClosed = False
        self.seq_num = None #Considerar Hacerlos Random
        self.ack = None     #Considerar Hacerlos Random

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
    
    def set_destination(self, host, port):
        self.dest_host = host
        self.dest_port = port
    #Devuelve una tupla con el paquete recibido, ya traducido y el address de donde vino
    def recv(self, timeout=0.5) -> Tuple[Packet, Tuple[str, int]] | None:
        self.socket.settimeout(timeout)
        timer = Chronometer()
        timer.start(timeout)
        while True:
            packet = Packet()
            try:
                packet_raw, address = self.socket.recvfrom(self.bufsize)
            except socket.timeout:
                return None
            packet.get(packet_raw)
            if (packet.tcp_dest_port == self.source_port):
                return (packet, address)
            self.socket.settimeout(timer.time_left)

    #Envia un paquete ya listo para enviar. Devuelve la cantidad de bits enviados
    def send(self, data) -> int:
        if self.dest_host == None:
            raise ConnException("No destination set for the socket " + self.host + " : " + self.port)
        return self.socket.sendto(data, (self.dest_host, self.dest_port))


class ConnException(Exception):
    pass
