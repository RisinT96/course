import struct
from contextlib import contextmanager


@contextmanager
def Timed(str):
    import time

    start = time.time()
    yield
    stop = time.time()

    print(f'{str} took {stop - start}s')


def counter_slow(length):
    return b''.join(struct.pack('H', x & 0xffff) for x in range(length))


def counter_medium(length):
    format_str = 'H' * length
    data = (x & 0xffff for x in range(length))
    return struct.pack(format_str, *data)


def counter_faster(length):
    format_str = 'H' * length
    data = [x & 0xffff for x in range(length)]
    return struct.pack(format_str, *data)


def counter_even_faster(length):
    format_str = f'{length}H'
    data = [x & 0xffff for x in range(length)]
    return struct.pack(format_str, *data)


def counter_even_more_faster(length):
    import array
    data = [x & 0xffff for x in range(length)]
    data_array = array.array('H', data)
    return data_array.tobytes()


def counter_ctypes(length):
    import ctypes

    ctypes_arr = (ctypes.c_uint16 * length)(*range(length))
    return bytes(ctypes_arr)


def counter_fast(length):
    import array
    rep_cnt = length // 0x10000
    modulo = length % 0x10000

    data = array.array('H', range(0x10000)).tobytes()

    arr_rep = data*rep_cnt
    return arr_rep + (data[:modulo*2])


with Timed('slow'):
    slow = counter_slow(10**7)

with Timed('medium'):
    medium = counter_medium(10**7)

with Timed('faster'):
    faster = counter_faster(10**7)

with Timed('even faster'):
    even_faster = counter_even_faster(10**7)

with Timed('even more faster'):
    even_more_faster = counter_even_more_faster(10**7)

with Timed('ctypes'):
    ctypes_res = counter_ctypes(10**7)

with Timed('fast'):
    fast = counter_fast(10**7)

print(slow == medium)
print(slow == faster)
print(slow == even_faster)
print(slow == even_more_faster)
print(slow == ctypes_res)
print(slow == fast)
