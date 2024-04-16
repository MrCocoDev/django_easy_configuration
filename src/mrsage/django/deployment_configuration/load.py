from mrsage.django.deployment_configuration.metadata import _APP


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
        get_library_setting,
    )
    from mrsage.django.deployment_configuration.magic import (
        replace_deployment_settings_module,
    )

    # Load all of our signals
    __import__(f"mrsage.django.deployment_configuration.signals")

    deployment_settings_module = load_deployment_settings_module(
        get_library_setting('deployment_settings_file')
    )
    generate_deployment_settings_safely(
        deployment_settings_module
    )
    if _APP['loaded'] == 'module':
        replace_deployment_settings_module(deployment_settings_module)
