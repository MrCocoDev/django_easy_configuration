from mrsage.django.deployment_configuration.django_cache_helpers import ttl_cache
from mrsage.django.deployment_configuration.django_settings_helpers import (
    get_library_setting,
)
from mrsage.django.deployment_configuration.exceptions import (
    LibraryIsImproperlyConfigured,
    MissingOptionInDatabase,
)
from mrsage.django.deployment_configuration.models import Option


def get_all_option_names():
    return set(Option.objects.all().values_list('name', flat=True))


def get_option_from_db(key):
    if key not in get_all_option_names():
        raise AttributeError(
            f"Deployment settings "
            f"'{get_library_setting('deployment_settings_file')}'"
            f" has no attribute '{key}'"
        )

    option = Option.objects.filter(name=key).first()
    if option:
        return option.value
    else:
        raise MissingOptionInDatabase("Could not find option in database, is the library loaded?")


if get_library_setting('use_cache'):
    cache_opts = {}
    for opt_key, key in {('ttl', 'cache_ttl'), ('cache_name', 'cache_name')}:
        try:
            cache_opts[opt_key] = get_library_setting(key)
        except LibraryIsImproperlyConfigured:
            ...

    get_option_from_db = ttl_cache(
        get_option_from_db,
        **cache_opts,
    )
