from conn import Conn
import utils

def listen(address: str) -> Conn:
    host, port = utils.parse_address(address)
    conn = Conn()
    conn.socket.bind(host, port)
    return conn

def accept(conn) -> Conn:
    pass


def dial(address) -> Conn:
    host, port = utils.parse_address(address)
    pass

def send(conn: Conn, data: bytes) -> int:
    pass


def recv(conn: Conn, length: int) -> bytes:
    pass


def close(conn: Conn):
    pass
