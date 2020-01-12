import struct

def counter(length):
    return b''.join(struct.pack('H', x & 0xffff) for x in range(length))

counter(10**7)

