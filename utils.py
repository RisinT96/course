class LazyStr:
    def __init__(self, func, *args, **kw):
        self.func = func
        self.args = args
        self.kw = kw

    def __str__(self):
        return str(func(*args, **kw))

