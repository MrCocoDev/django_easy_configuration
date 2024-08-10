from django.apps import AppConfig
from django.db.models.signals import post_migrate

from cocodev.django.deployment_configuration.exceptions import MissingTable
from cocodev.django.deployment_configuration.load import fully_load_library


def fully_load_library_after_migrations(sender, **kwargs):
    fully_load_library()


class DeploymentConfigurationConfig(AppConfig):
    default = True
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cocodev.django.deployment_configuration'

    def ready(self):
        try:
            fully_load_library()
        except MissingTable:
            """
            If migrations are running the first call will fail, but the
            post_migrate signal is only sent when migrations are running,
            so we can't use that normally.
            """
            post_migrate.connect(
                fully_load_library_after_migrations,
                sender=self,
            )


class DeploymentConfigurationTestConfig(AppConfig):
    """
    This exists just to not autoload settings during tests, which
    can make tests more difficult than necessary.
    """
    default = False
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cocodev.django.deployment_configuration'
