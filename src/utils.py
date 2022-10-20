import pickle
from typing import Any


def singleton(cls):
    instance = None
    def inner():
        nonlocal instance
        if not instance:
           instance = cls()
        return instance
    return inner


def load(file: str) -> Any:
    with open(file, 'rb') as f:
        obj = pickle.load(f)
    return obj


def dump(obj: Any, file: str):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)


def find_substr(string: str, sub: str):
    if len(sub) == 0:
        return True
    if len(string) == 0:
        return False
    assert len(sub) <= len(string), f'len substring[{len(sub)}] > len string[{len(string)}]'
    i, j = 0, 0
    while i < len(string) and j < len(sub):
        if sub[j] == string[i]:
            j += 1
        i += 1
    return True if j == len(sub) else False

