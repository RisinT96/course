import binascii
import logging
import sys

import utils

class Processor:
    def __init__(self):
        self.ones_count = self.twos_count = self.bad_packets = 0

    def _count_ones(self, data):
        result = 0
        for x in data:
            result += (x == '1')
        return result

    def _count_twos(self, data):
        result = 0
        for i in range(len(data)):
            result += (data[i] == '2')
        return result

    def process_packet(self, opcode, payload):
        logging.debug("Received packet %x %s", opcode, 
            utils.LazyStr(binascii.hexlify, payload.encode('utf8')))

        packet_ones = self._count_ones(payload)

        if opcode == 1:
            self.ones_count += packet_ones
            self.twos_count += self._count_twos(payload)
        else:
            self.bad_packets += 1

def main():
    log_level = logging.DEBUG if '-debug' in sys.argv else logging.ERROR
    logging.getLogger('').setLevel(log_level)
    processor = Processor()
    for opcode in range(4):
        for i in range(10):
            processor.process_packet(opcode, "This is a test" * 10000000)


main()

