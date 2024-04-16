from mrsage.django.deployment_configuration.django_settings_helpers import (
    get_library_setting,
)
from mrsage.django.deployment_configuration.exceptions import MissingOptionInDatabase
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
