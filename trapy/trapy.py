from conn import Conn
from state_of_send import State_of_Send
from tcp import *
from utils import *

def listen(address: str) -> Conn:
    host, port = utils.parse_address(address)
    conn = Conn()
    conn.bind(host, port)
    return conn

def accept(conn) -> Conn:
    syn_pack = receive_sync(conn)
    finish_handshake(conn, syn_pack)
    return conn

def dial(address) -> Conn:
    host, port = utils.parse_address(address)
    conn = Conn()
    conn.bind() #Lo ubico en un puerto libre
    conn.set_destination(host, port)
    send_sync(conn)
    send_confirmation(conn)
    return conn

def send(conn: Conn, data: bytes) -> int:
    chunks = fragment_data(data, conn.max_data_size)
    sent_data = 0
    for chunk in chunks:
        if send_chunk(conn, chunk):
            sent_data = sent_data + len(chunk)
        else:
            #Se enviaron bytes hasta q el receptor desaparecio
            return sent_data
    return sent_data



def recv(conn: Conn, length: int) -> bytes:
    pass


def close(conn: Conn):
    pass