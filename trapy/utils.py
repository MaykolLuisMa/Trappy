from struct import pack, unpack

def parse_address(address):
    host, port = address.split(':')

    if host == '':
        host = 'localhost'

    return host, int(port)

def make_checksum(data):
    length = len(data)
    checksum = 0
    for i in range(length//2):
        checksum += unpack('H', data[(2*i):(i*2)+2])[0]
        if (checksum >= 2**16): checksum -= 2**16
    if (length%2): checksum += unpack('H', data[(2*i):(i*2)+1])[0]
    if (checksum >= 2**16): checksum -= 2**16
    checksum += 1
    if (checksum >= 2**16): checksum -= 2**16
    return pack('H', checksum)

def corrupted(data, checksum):
    return checksum == make_checksum(data)