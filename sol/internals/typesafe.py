class typesafe(object):
    def __init__(self, type):
        super().__init__()
        self._type = type
        self._value = None

    def __get__(self, obj, type):
        return self._value

    def __set__(self, obj, value):
        if isinstance(value, self._type):
            self._value = value
        else:
            raise TypeError(
                f"Expected {self._type}, got {type(value)} ({value})")


class Test(object):
    def __init__(self):
        super().__init__()
        self.x = typesafe(int)
        self.y = typesafe(str)


test = Test()
test2 = Test()

test.x = 1
test.y = 'abc'

test2.x = 5
test2.y = 'def'

print(test.x)
print(test.y)
