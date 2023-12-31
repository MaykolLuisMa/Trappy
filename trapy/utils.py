from struct import pack, unpack
import socket

def parse_address(address):
    host, port = address.split(':')

    if host == '':
        host = 'localhost'

    return host, int(port)

def make_checksum(data):
    length = len(data)
    checksum = 0
    for i in range(length//2):
        checksum += unpack('!H', data[(2*i):(i*2)+2])[0]
        if (checksum >= 2**16): checksum -= 2**16
    if (length%2): checksum += unpack('!B', data[(length-1):])[0]
    if (checksum >= 2**16): checksum -= 2**16
    checksum += 1
    if (checksum >= 2**16): checksum -= 2**16
    return checksum

def get_free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0)) 
    port = sock.getsockname()[1]
    sock.close()
    return port

def corrupted(data, checksum):
    return checksum == make_checksum(data)