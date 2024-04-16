import functools
from types import FunctionType
from typing import Optional

from django.core.cache import caches


def ttl_cache(function: FunctionType = None, /, ttl: Optional[float] = None, cache_name: str = 'default'):
    """
    A TTL cache backed by Django's cache framework. See the CACHES setting
    for information on how the cache operates.

    https://docs.djangoproject.com/en/4.2/topics/cache/
    """
    # https://stackoverflow.com/a/74650070/1112794
    def decorator(func):
        key = func.__qualname__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = caches[cache_name].get(key)
            if not results:
                results = func(*args, **kwargs)
                caches[cache_name].set(key, results, ttl)

            return results

        wrapper.clear_cache = functools.partial(caches[cache_name].delete, key)

        return wrapper

    if function:
        return decorator(function)
    else:
        return decorator
