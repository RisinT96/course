from functools import wraps


def cahced(func):
    cache = {}

    def wrapped(*args):
        if args in cache:
            print('Cache hit!')
            return cache[args]

        res = func(*args)
        cache[args] = res

        return res

    return wrapped
