from collections import defaultdict


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError("No default factory provided!")
        self[key] = self.default_factory(key)
        return self[key]
