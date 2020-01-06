from collections import defaultdict


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        return super().default_factory(key)

a = keydefaultdict(int)

a[50] += 1
a[0x50] += 0x5

print(a['0']*10)
print(a['2']*10)
print(a['3']*10)
print(a[0x50])
