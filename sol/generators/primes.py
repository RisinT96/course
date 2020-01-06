from math import sqrt, floor
from itertools import islice


def is_prime(num):
    for i in range(2, floor(sqrt(num))+1):
        if num % i is 0:
            return False
    return True


def prime_generator():
    i = 1

    while(True):
        while (not is_prime(i)):
            i += 2

        yield i

        i += 2


def get_n_primes(num):
    return islice(prime_generator(), num)


def get_nth_primes(n_s, n_f):
    generator = prime_generator()

    for i in islice(generator, n_s):
        pass

    return islice(generator, n_f-n_s)


[print(i) for i in get_n_primes(10)]
[print(i) for i in get_nth_primes(100000, 100100)]
