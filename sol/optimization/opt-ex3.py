import binascii
import logging
import sys

class Processor:
    def __init__(self):
        self.ones_count = self.twos_count = self.bad_packets = 0

    def process_packet(self, opcode, payload):
        if(logging.getLogger('').getEffectiveLevel() <= logging.DEBUG):
            logging.debug("Received packet %x %s", opcode,
                          binascii.hexlify(payload.encode('utf8')))

        if opcode == 1:
            self.ones_count += payload.count('1')
            self.twos_count += payload.count('2')
        else:
            self.bad_packets += 1


def main():
    log_level = logging.DEBUG if '-debug' in sys.argv else logging.ERROR
    logging.getLogger('').setLevel(log_level)
    processor = Processor()
    for opcode in range(4):
        for i in range(10):
            processor.process_packet(opcode, "This is a test" * 100000)


main()
