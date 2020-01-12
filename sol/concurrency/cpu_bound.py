import time

from math import floor, sqrt
from contextlib import contextmanager


def is_prime(n):
    if n == 1:  # 1 is special
        return False

    divisors = range(2, floor(sqrt(n)))
    return all(n % d != 0 for d in divisors)


@contextmanager
def Timed(str):
    import time

    start = time.time()
    yield
    stop = time.time()

    print(f'{str} took {stop - start}s')


def calc_primes_threading(end, threads_num=1):
    import threading

    sol = []

    def worker(thread_id, total_threads, end):
        for i in range(thread_id, end, total_threads):
            if is_prime(i):
                sol.append(i)

    threads = []
    for i in range(threads_num):
        t = threading.Thread(target=worker, args=(i, threads_num, end))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    sol.sort()

    return sol


def worker(rng):
    primes = []

    for n in rng:
        if is_prime(n):
            primes.append(n)

    return primes


def calc_primes_dummy_pool(end, threads_num=1):
    from multiprocessing.dummy import Pool
    from heapq import merge

    ranges = [range(i+2, end, threads_num) for i in range(threads_num)]
    with Pool(threads_num) as p:
        res = p.map(worker, ranges)

    return res


def calc_primes_pool(end, threads_num=1):
    from multiprocessing import Pool
    from heapq import merge

    ranges = [range(i+2, end, threads_num) for i in range(threads_num)]
    with Pool(threads_num) as p:
        res = merge(p.map(worker, ranges))

    res

    return res


if __name__ == "__main__":
    # with Timed("1 thread"):
    #     calc_primes_threading(end=100000, threads_num=1)

    # with Timed("2 threads"):
    #     calc_primes_threading(end=100000, threads_num=2)

    # with Timed("Dummy pool sized 1"):
    #     list(calc_primes_dummy_pool(end=100000, threads_num=1))

    # with Timed("Dummy pool sized 2"):
    #     list(calc_primes_dummy_pool(end=100000, threads_num=2))

    with Timed("Pool sized 1"):
        list(calc_primes_pool(end=1000000, threads_num=1))

    with Timed("Pool sized 2"):
        list(calc_primes_pool(end=1000000, threads_num=2))

    with Timed("Pool sized 5"):
        list(calc_primes_pool(end=1000000, threads_num=4))
