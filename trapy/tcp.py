from conn import *
from aux_flags_functions import *
def receive_sync(conn : Conn):
    print("WAITING SYNC")
    sync_packet = wait_packet_with_condition(conn, is_sync)
    conn.set_destination(sync_packet.ip_source_host, sync_packet.tcp_source_port)
    print("RECEIVED SYNC")
    return sync_packet

def finish_handshake(conn: Conn):
    sync_ack_packet = create_packet(conn)
    sync_ack_packet.flags = 18 # ACK + SYNC
    data = sync_ack_packet.build()
    for i in range(0, 20):
        conn.send(data)
    print("WAITING CONFIRMATION")
    wait_packet_with_condition(conn, is_sync_ack)
    print("HANDSHAKE IS OVER")

def send_sync(conn : Conn):
    sync_packet = create_packet(conn)
    sync_packet.flags = 2 #SYNC
    data = sync_packet.build()
    for i in range(0, 20):
        conn.send(data)

def wait_sync_ack(conn : Conn):
    print("WAITING SYNC ACK")
    wait_packet_with_condition(conn, is_sync_ack)
    print("RECEIVED SYNC ACK")

def send_confirmation(conn):
    conf_packet = create_packet(conn)
    conf_packet.flags = 18 #ACK + SYNC
    data = conf_packet.build()
    for i in range(0, 20):
        conn.send(data)

def wait_packet_with_condition(conn : Conn, cond = always, timeout = 5): #Q tiempo ponemos default el timeout?
    timer = Chronometer()
    timer.start()
    while True:
        packet = conn.recv()[0]
        if (packet is None) or not(cond(packet.flags)):
            if timer.timeout():
                raise ConnectionError("Connection TimeOut at HandShaking")
            continue
        conn.ack = packet.tcp_seq_num
        conn.seq_num = packet.tcp_ack_num + 1
        return packet

def create_packet(conn : Conn):
    packet = Packet()
    packet.update(
        ip_dest_host= conn.dest_host,
        ip_source_host= conn.source_host,
        tcp_dest_port= conn.dest_port,
        tcp_source_port = conn.source_port,
        tcp_seq_num= conn.seq_num,
        tcp_ack_num= conn.ack,
    )
    return packet