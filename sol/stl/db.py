import pickle
import shelve


class DB(object):
    def __init__(self, path: str):
        super().__init__()

        self.db_path = path

        try:
            with open(path, 'rb') as file:
                self.db = pickle.load(file)
        except Exception:
            self.db = {}

    def closed(self, *args):
        raise ValueError('invalid operation on closed db')

    def close(self):
        with open(self.db_path, 'wb') as file:
            pickle.dump(self.db, file)
        self.db = None
        self.db_path = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getitem__(self, key):
        if self.db is None:
            raise RuntimeError('This DB is not initialized')

        return self.db[key]

    def __setitem__(self, key, value):
        if self.db is None:
            raise RuntimeError('This DB is not initialized')

        self.db[key] = value
        return value


db = DB('ass.bin')

db['a'] = 5
db['b'] = 5
db['b'] = 5
db['a'] = 5

db.close()

db = DB('ass.bin')

with DB('abc') as db:
    db['a'] = 10
    db['b'] = [1, 2, 3, 4, 5, 56, 6, 7]

with DB('abc') as db:
    print(db['a'])
    print(db['b'])
