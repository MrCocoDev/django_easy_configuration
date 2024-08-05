import logging

from django.db import OperationalError

from mrsage.django.deployment_configuration.exceptions import MissingTable

log = logging.getLogger(__name__)
SHOULD_LOAD = True


def fully_load_library():
    """
    Fully loads the library and slides the deployment
    Returns:
    """
    from mrsage.django.deployment_configuration.core import (
        generate_deployment_settings_safely,
        load_deployment_settings_module,
    )
    from mrsage.django.deployment_configuration.django_settings_helpers import (
        LIBRARY_SETTINGS,
    )
    from mrsage.django.deployment_configuration.magic import (
        replace_deployment_settings_module,
    )
    from mrsage.django.deployment_configuration.metadata import _APP

    # Load all of our signals
    __import__(f"mrsage.django.deployment_configuration.signals")

    deployment_settings_module = load_deployment_settings_module(
        LIBRARY_SETTINGS.deployment_settings_file
    )
    generate_deployment_settings_safely(
        deployment_settings_module
    )
    if _APP['loaded'] == 'module':
        try:
            replace_deployment_settings_module(deployment_settings_module)
        except OperationalError as e:
            from mrsage.django.deployment_configuration.models import Option
            if (
                    f"no such table: {Option._meta.db_table}"
                    in repr(e)
            ):
                raise MissingTable("Migrations need to be run!") from e
