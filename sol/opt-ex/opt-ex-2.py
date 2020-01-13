import pstats
import cProfile
import struct
import time
from collections import defaultdict


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError("No default factory provided!")
        self[key] = self.default_factory(key)
        return self[key]


class Encoder():
    MAGIC_NUMBER = 24
    PACKED_MAGIC = struct.pack('<H', MAGIC_NUMBER)
    SIZE_DICT = keydefaultdict(lambda x: struct.pack('<L', x))
    CACHE = keydefaultdict(
        lambda x: Encoder.PACKED_MAGIC + struct.pack('<L', x))

    def encode(self, payload):
        magic = struct.pack('<H', self.MAGIC_NUMBER)
        size = struct.pack('<L', len(payload))
        packet = magic + size + payload
        return packet

    def encode3(self, payload):
        size = struct.pack('<L', len(payload))
        packet = self.PACKED_MAGIC + size + payload
        return packet

    def encode4(self, payload):
        size = self.SIZE_DICT[len(payload)]
        packet = self.PACKED_MAGIC + size + payload
        return packet

    def encode5(self, payload):
        size = self.SIZE_DICT[len(payload)]
        return b''.join([self.PACKED_MAGIC, size, payload])

    def encode6(self, payload):
        magic_size = self.CACHE[len(payload)]
        return b''.join([magic_size, payload])

    def encode7(self, payload):
        magic_size = self.CACHE[len(payload)]
        return magic_size + payload

    def encode8(self, payload):
        return self.CACHE[len(payload)] + payload


def main(payloads):
    encoder = Encoder()

    result = []
    for payload in payloads:
        result.append(encoder.encode(payload))

    return result


def main2(payloads):
    encoder = Encoder()

    return [encoder.encode(payload) for payload in payloads]


def main3(payloads):
    encoder = Encoder()

    return [encoder.encode3(payload) for payload in payloads]


def main4(payloads):
    encoder = Encoder()

    return [encoder.encode4(payload) for payload in payloads]


def main5(payloads):
    encoder = Encoder()

    return [encoder.encode5(payload) for payload in payloads]


def main6(payloads):
    encoder = Encoder()

    return [encoder.encode6(payload) for payload in payloads]


def main7(payloads):
    encoder = Encoder()

    return [encoder.encode7(payload) for payload in payloads]


def main8(payloads):
    encoder = Encoder()

    return [encoder.encode8(payload) for payload in payloads]


payloads = [str(i).encode('utf8') for i in range(10**6)]
if __name__ == '__main__':
    import timeit


    print(timeit.timeit('main(payloads)', setup='from __main__ import main, Encoder, payloads', number=10))
    res = main(payloads)

    print(timeit.timeit('main2(payloads)', setup='from __main__ import main2, Encoder, payloads', number=10))
    res2 = main2(payloads)

    print(timeit.timeit('main3(payloads)', setup='from __main__ import main3, Encoder, payloads', number=10))
    res3 = main3(payloads)

    print(timeit.timeit('main4(payloads)', setup='from __main__ import main4, Encoder, payloads', number=10))
    res4 = main4(payloads)

    print(timeit.timeit('main5(payloads)', setup='from __main__ import main5, Encoder, payloads', number=10))
    res5 = main5(payloads)

    print(timeit.timeit('main6(payloads)', setup='from __main__ import main6, Encoder, payloads', number=10))
    res6 = main6(payloads)

    print(timeit.timeit('main7(payloads)', setup='from __main__ import main7, Encoder, payloads', number=10))
    res7 = main7(payloads)

    print(timeit.timeit('main8(payloads)', setup='from __main__ import main8, Encoder, payloads', number=10))
    res8 = main8(payloads)

    print(res8 == res7 == res6 == res5 == res4 == res3 == res2 == res)
