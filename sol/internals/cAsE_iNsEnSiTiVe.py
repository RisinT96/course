class CaSeInSeNsItIvE(object):
    def __setattr__(self, name, value):
        self.__dict__[name.lower()] = value

    def __getattr__(self, name):
        try:
            return self.__dict__[name.lower()]
        except KeyError as e:
            raise AttributeError(f"{self} has no attribute '{name}'")


a = CaSeInSeNsItIvE()

a.x = 5
print(a.X)

a.xYddsfSDf = 234908234908
print(a.xyddsfsdf)

a.dsf

print(a.__dict__)
