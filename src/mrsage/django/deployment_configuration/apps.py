from django.apps import AppConfig


class DeploymentConfigurationConfig(AppConfig):
    default = True
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mrsage.django.deployment_configuration'

    def ready(self):
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

        deployment_settings_module = load_deployment_settings_module(
            get_library_setting('deployment_settings_file')
        )
        generate_deployment_settings_safely(
            deployment_settings_module
        )
        replace_deployment_settings_module(deployment_settings_module)


class DeploymentConfigurationTestConfig(AppConfig):
    """
    This exists just to not autoload settings during tests, which
    can make tests more difficult than necessary.
    """
    default = False
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mrsage.django.deployment_configuration'
