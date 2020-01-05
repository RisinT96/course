from contextlib import contextmanager


@contextmanager
def Timed(str):
    import time

    start = time.time()
    yield
    stop = time.time()

    print(f'{str} took {stop - start}s')
