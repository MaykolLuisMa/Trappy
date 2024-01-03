from conn import Conn
from tcp import *
from utils import *

def listen(address: str) -> Conn:
    host, port = utils.parse_address(address)
    conn = Conn()
    conn.bind(host, port)
    return conn

def accept(conn) -> Conn:
    syn_pack = receive_sync(conn)
    finish_handshake(conn)
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
    idx = 1
    for chunk in chunks:
        if send_chunk(conn, chunk, (idx == len(chunks))):
            sent_data = sent_data + len(chunk)
            idx = idx + 1
        else:
            #Se llega aqui si se recibio un fin, o si se desconecto el receptor
            send_fin_conf(conn)
            return sent_data
    #Realmente no hay manera d q se llegue aqui abajo

def recv(conn: Conn, length: int) -> bytes:
    buffer = b''
    print("buffer len")
    print(len(buffer))
    packet = wait_packet_with_condition(conn, is_expected_data, 2)
    if packet is None:
        raise ConnException("Nunca llego el primer paquete")
    keep_going = True
    while ((len(buffer) < length) and keep_going):
        if is_fin(conn, packet):
            keep_going = False
        if packet is None:
            raise ConnException("Se desconecto el emisor")
        if(not is_empty(conn,packet)):
            buffer = buffer + packet.data
        print("sequence number")
        print(packet.tcp_seq_num)
        packet = next_data(conn, not(keep_going)) #dentro de next data mandamos el ack
    return trim(buffer, length) #Reducir lo leido al tamanho solicitado
        
        

def close(conn: Conn):
    pass
