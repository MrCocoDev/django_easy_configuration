"""
The non-magic way of accessing the values
"""

from mrsage.django.deployment_configuration.retrieve import get_option_from_db


def __getattr__(name):
    return get_option_from_db(name)
