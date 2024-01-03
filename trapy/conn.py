import socket
import os
from chronometer import *
from packet import *
from typing import Tuple
from random import randint
from utils import get_free_port

class Conn:    
    def __init__(self, sock=None):
        if sock is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.max_data_size = 512
        self.bufsize = 20 + 20 + self.max_data_size
        self.source_host = None
        self.source_port = None
        self.dest_host = None
        self.dest_port = None
        self.isClosed = False
        self.seq_num = 0 #Los inicializare durante el handshake
        self.ack_num = 0 #Los inicializare durante el handshake

        self.socket = sock

    def close(self):
        #Aqui reiniciaremos todos los atributos
        self.socket.close()
        self.host = None
        self.port = None
        self.isClosed = True
    
    def bind(self, host = None, port = None):
        if (host == None):
            host = '127.0.0.1'
        self.source_host = host
        if (port == None):
            port = get_free_port()
        self.socket.bind((self.source_host, port))
        #print("---------------- " + str(port))
        #print(self.socket.getsockname())
        #self.source_port = self.socket.getsockname()[1] #Averiguando que puerto fue asignado
        self.source_port = port

    def set_destination(self, host, port):
        self.dest_host = host
        self.dest_port = port
    #Devuelve una tupla con el paquete recibido, ya traducido y el address de donde vino
    def recv(self, timeout=0.5, unknwn_source=False) -> Tuple[Packet | None, Tuple[str, int] | None]:
        self.socket.settimeout(timeout)
        timer = Chronometer()
        timer.start(timeout)
        while True:
            packet = Packet()
            try:
                packet_raw, address = self.socket.recvfrom(self.bufsize)
            except socket.timeout:
                return (None, None)
            packet.get(packet_raw)
            #print("Llego un paquete de " + packet.source_ip +" : " + str(packet.tcp_source_port))
            #print("El paquete venia destinado a " + packet.dest_ip + " " + str(packet.tcp_dest_port))
            if ((packet.tcp_dest_port == self.source_port) or unknwn_source):
                return (packet, address)
            self.socket.settimeout(timer.time_left())

    #Envia un paquete ya listo para enviar. Devuelve la cantidad de bits enviados
    def send(self, data) -> int:
        if self.dest_host == None:
            raise ConnException("No destination set for the socket " + self.host + " : " + self.port)
        address = (self.dest_host, self.dest_port)
        #print("Enviado un paquete a " + address[0] + ":" + str(address[1]))
        #print("Yo soy " + self.source_host + " " + str(self.source_port)
        # )
        #print("data-----")
        #print(data)
        #print("-----data")
        return self.socket.sendto(data, address)


class ConnException(Exception):
    pass
