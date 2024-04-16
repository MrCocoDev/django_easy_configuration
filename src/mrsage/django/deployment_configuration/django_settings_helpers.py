from unittest.mock import sentinel

from django.conf import settings

from mrsage.django.deployment_configuration.exceptions import (
    LibraryIsImproperlyConfigured,
)

notset = sentinel.notset


def get_library_setting(key, default=notset):
    try:
        settings.DEPLOYMENT_CONFIGURATION_SETTINGS[key]
    except:
        if default is not notset:
            return default
        else:
            raise LibraryIsImproperlyConfigured(
                f"You must set {key} in the DEPLOYMENT_CONFIGURATION_SETTINGS "
                f"settings dict for the library to function"
            )
