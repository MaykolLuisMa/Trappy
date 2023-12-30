from conn import *
from aux_flags_functions import *
def receive_sync(conn : Conn):
    sync_packet = wait_packet_with_condition(conn, is_sync)
    conn.set_destination(sync_packet.ip_source_host, sync_packet.tcp_source_port)
    return sync_packet

def finish_handshake(conn: Conn):
    sync_ack_packet = create_packet(conn)
    sync_ack_packet.flags = 18 # ACK + SYNC
    conn.send(sync_ack_packet.build())
    wait_packet_with_condition(conn, is_sync_ack)

def send_sync(conn : Conn):
    sync_packet = create_packet(conn)
    sync_packet.flags = 2 #SYNC
    conn.send(sync_packet.build())

def wait_sync_ack(conn : Conn):
    wait_packet_with_condition(conn, is_sync_ack)

def send_confirmation(conn):
    conf_packet = create_packet(conn)
    conf_packet.flags = 18 #ACK + SYNC
    conn.send(conf_packet.build())

def wait_packet_with_condition(conn : Conn, cond = always):
    while True:
        packet = conn.recv()[0]
        if (packet is None) or not(cond(packet.flags)):
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