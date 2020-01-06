import orjson
import json
from contextlib import contextmanager


@contextmanager
def Timed(str):
    import time

    start = time.time()
    yield
    stop = time.time()

    print(f'{str} took {stop - start}s')


with Timed('json loads'):
    for i in range(1000):
        with open("github.json", 'r') as f:
            loaded_json = json.loads(f.read())

with Timed('json load'):
    for i in range(1000):
        with open("github.json", 'r') as f:
            loaded_json = json.load(f)

with Timed('orjson loads'):
    for i in range(1000):
        with open("github.json", 'r') as f:
            loaded_orjson = orjson.loads(f.read())

with Timed('json dumps'):
    for i in range(1000):
        with open("github.json,out", 'w') as f:
            f.write(json.dumps(loaded_json))

with Timed('json dump'):
    for i in range(1000):
        with open("github.json.out", 'w') as f:
            json.dump(loaded_json, f)

with Timed('orjson dumps'):
    for i in range(1000):
        with open("github.json.out", 'wb') as f:
            f.write(orjson.dumps(loaded_json))
