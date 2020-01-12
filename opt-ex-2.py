import struct
import time

class Encoder():
    MAGIC_NUMBER=24
    
    def encode(self,payload):
        magic = struct.pack('<H',self.MAGIC_NUMBER)
        size = struct.pack('<L',len(payload))
        packet = magic + size + payload
        return packet

def main (payloads):
    encoder = Encoder()

    result=[]
    for payload in payloads:
        result.append(encoder.encode(payload))

    return result

payloads=[str(i).encode('utf8') for i in range(10**6)]

start_time=time.time()
main(payloads)
print(time.time()-start_time)
