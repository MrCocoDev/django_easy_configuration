import functools
from functools import _make_key
from typing import Callable, Optional

from django.core.cache import caches


def ttl_cache(function: Callable = None, /, ttl: Optional[float] = None, cache_name: str = 'default'):
    """
    A TTL cache backed by Django's cache framework. See the CACHES setting
    for information on how the cache operates.

    https://docs.djangoproject.com/en/4.2/topics/cache/
    """

    def get_cache():
        return caches[cache_name]

    def clear_cache(key=None):
        """
        Perhaps allowing the clearing the entire cache is dangerous
        """
        if key:
            return get_cache().delete(key)
        else:
            return get_cache().clear()

    # https://stackoverflow.com/a/74650070/1112794
    def decorator(func):

        def make_key(*args, **kwargs):
            return str(
                _make_key((func.__module__, func.__qualname__, *args), kwargs, typed=False)
            ).replace(
                '[', '_bo_'
            ).replace(
                ']', '_bc_'
            ).replace(
                ' ',
                '',
            )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = make_key(*args, **kwargs)
            results = caches[cache_name].get(key)
            if not results:
                results = func(*args, **kwargs)
                caches[cache_name].set(key, results, ttl)

            return results

        wrapper.clear_cache = clear_cache
        wrapper.get_cache = get_cache
        wrapper.make_key = make_key

        return wrapper

    if function:
        return decorator(function)
    else:
        return decorator
