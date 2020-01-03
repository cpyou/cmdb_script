import functools


def task(*dargs, **dkwargs):
    print(dargs, dkwargs)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(args, kwargs)
            res = func(*args, **kwargs)
            return res
        return wrapper
    return decorator


@task(key='assd')
def f(a=1):
    print(a)
    return a


f(a=1)
