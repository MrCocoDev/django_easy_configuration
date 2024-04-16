import logging

from mrsage.django.deployment_configuration.retrieve import get_option_from_db

log = logging.getLogger(__name__)

MAGICKED_MODULE = None


def replace_deployment_settings_module(module):
    module.__getattr__ = get_option_from_db

    global MAGICKED_MODULE
    if MAGICKED_MODULE and MAGICKED_MODULE != module:
        log.error("Applying module magic twice may result in strange behavior and bugs!")

    MAGICKED_MODULE = module
