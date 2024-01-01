from conn import Conn
from packet import Packet
def always(conn: Conn, packet: Packet):
    return True
def is_sync(conn : Conn, packet: Packet):
    return ((packet.tcp_flags & 2) > 0)
def is_ack(conn : Conn, packet: Packet):
    return (((packet.tcp_flags & 16) > 0) and (conn.seq_num + 1 == packet.tcp_ack_num))
def is_sync_ack(conn : Conn, packet: Packet):
    return (is_ack(conn, packet) and is_sync(packet))
def is_fin(packet: Packet):
    return ((packet.tcp_flags & 1) > 0)