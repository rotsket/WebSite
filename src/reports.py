import functools
import re


def roports():
    def my_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pass
        return wrapper
    return my_decorator

