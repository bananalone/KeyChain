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
