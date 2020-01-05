from contextlib import contextmanager


@contextmanager
def NoExceptions(*args):
    try:
        yield
    except args as e:
        print(f"Caught exception: {type(e)}:'{e}'")
        pass


with NoExceptions(ZeroDivisionError, EnvironmentError):
    raise ZeroDivisionError("what?! are u mad?")
