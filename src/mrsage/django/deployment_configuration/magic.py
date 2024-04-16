import logging

from mrsage.django.deployment_configuration.exceptions import MissingOptionInDatabase
from mrsage.django.deployment_configuration.models import Option

log = logging.getLogger(__name__)

OPTION_NAMES = set()
MAGICKED_MODULE = None


def replace_deployment_settings_module(module):
    option_names = module.__annotations__.keys()
    for option_name in option_names:
        delattr(module, option_name)
        OPTION_NAMES.add(option_name)

    module.__getattr__ = get_option_from_db

    global MAGICKED_MODULE
    if MAGICKED_MODULE and MAGICKED_MODULE != module:
        log.error("Applying module magic twice may result in strange behavior and bugs!")

    MAGICKED_MODULE = module


def get_option_from_db(key):
    if key not in OPTION_NAMES:
        raise AttributeError(f"module '{MAGICKED_MODULE.__name__}' has no attribute '{key}'")

    option = Option.objects.filter(name=key).first()
    if option:
        return option.value
    else:
        raise MissingOptionInDatabase("Could not find option in database, is the library loaded?")
