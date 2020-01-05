from functools import wraps


def debug(func):
    def decorated_func(*a, **k):
        print(f'Calling "{func.__name__}" with args {a} {k}')
        try:
            ret = func(*a, **k)
        except Exception as e:
            print(f'"{func.__name__}" raised exception {type(e)}: "{e}"')
            raise e
        else:
            print(f'"{func.__name__}" returned "{ret}"')
            return ret

    return decorated_func


@debug
def div100by(x):
    return 100/x
