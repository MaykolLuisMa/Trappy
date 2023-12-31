def always(conn: Conn):
    return True
def is_sync(conn: Conn):
    return ((conn.flags & 2) > 0)
def is_ack(conn: Conn):
    return ((conn.flags & 16) > 0)
def is_sync_ack(conn: Conn):
    return (is_ack(conn.flags) and is_sync(conn.flags))