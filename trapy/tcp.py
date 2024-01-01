from conn import *
from aux_flags_functions import *

#Handshaking
def receive_sync(conn : Conn):
    print("WAITING SYNC")
    sync_packet = wait_packet_with_condition(conn, is_sync)
    conn.seq_num = randint(1, 1000)
    conn.set_destination(sync_packet.ip_source_host, sync_packet.tcp_source_port)
    print("RECEIVED SYNC")
    return sync_packet

def finish_handshake(conn: Conn):
    sync_ack_packet = create_packet(conn)
    sync_ack_packet.flags = 18 # ACK + SYNC
    send_till_its_received(conn, sync_ack_packet, is_sync_ack)

def send_sync(conn : Conn):
    conn.seq_num = randint(1, 1000)
    sync_packet = create_packet(conn)
    sync_packet.flags = 2 #SYNC
    send_till_its_received(conn, sync_packet, is_sync_ack)

def send_confirmation(conn):
    conf_packet = create_packet(conn)
    conf_packet.flags = 16 #ACK
    send_many_times(conf_packet)


#Transmission
def send_chunk(conn : Conn, chunk, is_last_chunk):
    packet = create_packet(conn)
    packet.data = chunk
    if is_last_chunk:
        packet.tcp_flags = 1 #FIN
    ack_packet = send_till_its_received(conn, packet, is_ack, 2)
    return not(is_fin(ack_packet))

def send_fin_conf(conn : Conn):
    fin_conf_packet = create_packet(conn)
    fin_conf_packet.flags = 17 #ACK + FIN
    send_many_times(fin_conf_packet)


#Global Utils
def send_till_its_received(conn : Conn, packet : Packet, cond = always, timeout = None):
    data = packet.build()
    timer = None
    idx = 0
    if timeout is not None:
        timer = Chronometer()
        timer.start(timeout)
    while True:
        if timeout is None:
            idx = idx + 1
        if ((idx == 10) or ((timeout is not None) and timer.timeout())):
            break
        conn.send(data)
        ack_packet = wait_packet_with_condition(conn, cond)
        if ack_packet is not None:
            return ack_packet
    if ((timeout is not None) and (timer.timeout())):
        return None
    raise ConnException("Conexion's Lost")

def send_many_times(conn : Conn, packet : Packet):
    data = packet.build()
    for i in range(0, 20):
        conn.send(data)

def wait_packet_with_condition(conn : Conn, cond = always, timeout = 5): #Q tiempo ponemos default el timeout?
    timer = Chronometer()
    timer.start()
    while True:
        packet = conn.recv()[0]
        if (packet is None) or not(cond(conn, packet)):
            if timer.timeout():
                return None
            continue
        conn.ack_num = packet.tcp_seq_num + 1 #Decidimos no sumar la longitud del paquete, sino siempre sumar 1
        conn.seq_num = packet.tcp_ack_num
        return packet

def create_packet(conn : Conn):
    packet = Packet()
    packet.update(
        ip_dest_host= conn.dest_host,
        ip_source_host= conn.source_host,
        tcp_dest_port= conn.dest_port,
        tcp_source_port = conn.source_port,
        tcp_seq_num= conn.seq_num,
        tcp_ack_num= conn.ack_num,
    )
    return packet