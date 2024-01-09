from conn import Conn
from packet import Packet
def always(conn: Conn, packet: Packet):
    return True
def is_sync(conn : Conn, packet: Packet):
    return ((packet.tcp_flags & 2) > 0 and not packet.corrupted())
def is_ack(conn : Conn, packet: Packet):
    return (((packet.tcp_flags & 16) > 0) and (conn.seq_num + 1 == packet.tcp_ack_num) and not packet.corrupted())
def is_sync_ack(conn : Conn, packet: Packet):
    return (is_ack(conn, packet) and is_sync(conn, packet) and not packet.corrupted())
def is_fin(conn : Conn, packet: Packet):
    return ((packet.tcp_flags & 1) > 0 and not packet.corrupted())
def is_expected_data(conn : Conn, packet : Packet):
    return (packet.tcp_seq_num == conn.ack_num and not packet.corrupted())
def has_ack_flag(conn : Conn, packet : Packet):
    return ((packet.tcp_flags & 16) > 0 and not packet.corrupted())