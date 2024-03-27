#!/usr/bin/env python3
"""Module."""

import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Function counts how many times methods of the Cache class
        are called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Function store the history of inputs and outputs for
        a particular function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        result = method(self, *args)
        # adding the result to the list
        self._redis.rpush(f"{method.__qualname__}:outputs", result)
        return result
    return wrapper


def replay(method: Callable) -> None:
    """Function displays the history of calls of a particular function."""
    # access redis instance stored in method's object
    method_name = method.__qualname__
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"
    redis_instance = method.__self__._redis
    num_methods = redis_instance.get(method_name).decode('utf-8')
    print(f"{method_name} was called {num_methods} times:")

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    for inp_data, out_data in zip(inputs, outputs):
        inp_val, out_val = inp_data.decode("utf-8"), out_data.decode("utf-8")
        print(f"{method_name}(*{inp_val}) -> {out_val}")


class Cache:
    """Contains __init__ and store methods."""

    def __init__(self) -> None:
        """Function stores an instance of the Redis client as _redis
        using redis.Redis() and flushes the instances using flushdb."""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Function takes a data arg and returns a string."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Function takes a key string argument and an optional Callable
        argument fn will be used to convert data back to desired format."""
        if not self._redis.exists(key):
            return None
        if fn is not None:
            data = self._redis.get(key)
            return fn(data)
        else:
            return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """Function converts bytes to string."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Function converts bytes to integer."""
        return self.get(key, lambda x: int(x))
