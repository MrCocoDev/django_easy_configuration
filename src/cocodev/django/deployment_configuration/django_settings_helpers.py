from unittest.mock import sentinel

from django.conf import settings

from cocodev.django.deployment_configuration.exceptions import (
    LibraryIsImproperlyConfigured,
)

notset = sentinel.notset


def get_library_setting(key, default=notset):
    try:
        return settings.DEPLOYMENT_CONFIGURATION_SETTINGS[key]
    except:
        if default is not notset:
            return default
        else:
            raise LibraryIsImproperlyConfigured(
                f"You must set {key} in the DEPLOYMENT_CONFIGURATION_SETTINGS "
                f"settings dict for the library to function"
            )


class LibrarySettings:
    @property
    def use_cache(self):
        return get_library_setting('use_cache', True)

    @property
    def deployment_settings_file(self):
        return get_library_setting('deployment_settings_file')

    @property
    def cache_name(self):
        return get_library_setting('cache_name', 'default')

    @property
    def cache_ttl(self):
        return get_library_setting('cache_ttl', None)


LIBRARY_SETTINGS = LibrarySettings()
