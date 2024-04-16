from django.apps import AppConfig

from mrsage.django.deployment_configuration.load import fully_load_library


class DeploymentConfigurationConfig(AppConfig):
    default = True
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mrsage.django.deployment_configuration'

    def ready(self):
        fully_load_library()


class DeploymentConfigurationTestConfig(AppConfig):
    """
    This exists just to not autoload settings during tests, which
    can make tests more difficult than necessary.
    """
    default = False
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mrsage.django.deployment_configuration'
