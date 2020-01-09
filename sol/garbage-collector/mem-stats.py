from collections import Counter

import gc


def print_mem_stats(top=10):
    objects_list = (type(obj) for obj in gc.get_objects())
    objects_count = Counter(objects_list).most_common(top)
    [print(f'{v}: {k}') for k, v in objects_count]

print_mem_stats(5)

print_mem_stats()

print_mem_stats(1080)