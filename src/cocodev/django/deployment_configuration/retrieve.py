__all__ = [
    "get_all_option_names",
    "get_option_from_db",
]

from cocodev.django.deployment_configuration.django_cache_helpers import ttl_cache
from cocodev.django.deployment_configuration.django_settings_helpers import (
    LIBRARY_SETTINGS,
)
from cocodev.django.deployment_configuration.exceptions import (
    LibraryIsImproperlyConfigured,
    MissingOptionInDatabase,
)
from cocodev.django.deployment_configuration.models import Option


def get_all_option_names():
    return set(Option.objects.all().values_list('name', flat=True))


def get_option_from_db(key):
    if key not in get_all_option_names():
        raise AttributeError(
            f"Deployment settings "
            f"'{LIBRARY_SETTINGS.deployment_settings_file}'"
            f" has no attribute '{key}'"
        )

    option = Option.objects.filter(name=key).first()
    if option:
        return option.value
    else:
        raise MissingOptionInDatabase("Could not find option in database, is the library loaded?")


if LIBRARY_SETTINGS.use_cache:
    _cache_opts = {}
    for _opt_key, _key in {('ttl', 'cache_ttl'), ('cache_name', 'cache_name')}:
        try:
            _cache_opts[_opt_key] = getattr(LIBRARY_SETTINGS, _key)
        except LibraryIsImproperlyConfigured:
            ...

    get_option_from_db = ttl_cache(
        get_option_from_db,
        **_cache_opts,
    )
