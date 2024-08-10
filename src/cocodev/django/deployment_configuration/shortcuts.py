from cocodev.django.deployment_configuration.core import load_deployment_settings_module
from cocodev.django.deployment_configuration.django_settings_helpers import (
    LIBRARY_SETTINGS,
)


def module_from_library_settings():
    return load_deployment_settings_module(
        LIBRARY_SETTINGS.deployment_settings_file
    )
