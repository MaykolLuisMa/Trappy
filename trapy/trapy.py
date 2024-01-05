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
    if conn.isClosed:
        raise ConnException("La conexion esta cerrada")
    chunks = create_queue(data, conn.max_data_size)
    sent_data = 0
    keep_going = True
    last_received = conn.seq_num
    while (not(chunks.empty()) and keep_going):
        ack_packet = send_n_chunks(conn, chunks)
        while (last_received < ack_packet.tcp_ack_num):
            sent_data = sent_data + len(chunks.peek())
            chunks.pop()
            last_received = last_received + 1
        keep_going = not(is_fin(conn, ack_packet))
    send_confirmation(conn)
    return sent_data

#Si uso trim, debo dejar claro que hubo un paquete que recibi bien pero no trabaje completo y por tanto perdi parte
#Notemos que si deja de recibir un paquete, ahi mismo no procesa los siguientes, para preservar el orden
def recv(conn: Conn, length: int) -> bytes:
    if conn.isClosed:
        raise ConnException("La conexion esta cerrada")
    buffer = b''
    timer = Chronometer()
    keep_going = True
    packet = None
    while keep_going:
        timer.start(MAXIMUM_WAIT_BEFORE_ACK)
        for i in range(0, N_CHUNKS_PER_ACK):
            if ((i > 0) or (packet == None)):
                packet = wait_packet_with_condition(conn, is_expected_data, timer.time_left())
            if packet is not None:
                buffer = buffer + packet.data
                if (is_fin(conn, packet) or (len(buffer) > length)):
                    keep_going = False
                    break
            break #Caso en el q se agoto el timer
        packet = next_data(conn, not(keep_going))
    return trim(buffer, length)

def close(conn: Conn):
    conn.close()