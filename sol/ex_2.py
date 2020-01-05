from functools import wraps


def typesafe(**kwarg_types):
    def decorator(func):
        arg_types = [kwarg_types[arg_name]
                     for arg_name in func.__code__.co_varnames]

        args_num = len(arg_types)

        def decorated(*args, **kwargs):
            if (len(args) + len(kwargs)) != args_num:
                raise TypeError(
                    f"Expected {args_num} arguments, got {len(args) + len(kwargs)}")

            for key in kwargs:
                if(key not in kwarg_types):
                    raise TypeError(
                        f"Invalid argument '{key}'")

                if(not isinstance(kwargs[key], kwarg_types[key])):
                    raise TypeError(
                        f"Expected {kwarg_types[key]} got {type(kwargs[key])} for kwargument '{key}'")

            for idx, (arg_type, arg) in enumerate(zip(arg_types, args)):
                if(not isinstance(arg, arg_type)):
                    raise TypeError(
                        f"Expected {arg_type} got {type(arg)} for argument {idx}")

            return func(*args, **kwargs)
        return decorated
    return decorator


@typesafe(x=int, y=int)
def foo(x, y):
    return x+y


@typesafe(x=int, y=int, z=float)
def foo3(x, y, z):
    return (x+y)*z


foo(1, 2)
foo(1, 5)
foo(x=1, y=2)
foo(1, y=2)

try:
    foo('1', 2)
except Exception as e:
    print(e)

try:
    foo(1, '2')
except Exception as e:
    print(e)

try:
    foo(x='1', y=2)
except Exception as e:
    print(e)

try:
    foo(y='1', x=2)
except Exception as e:
    print(e)

try:
    foo(1, y='2')
except Exception as e:
    print(e)

try:
    foo(1, x=1, y='2')
except Exception as e:
    print(e)

try:
    foo3(1, x=1, t='2')
except Exception as e:
    print(e)
