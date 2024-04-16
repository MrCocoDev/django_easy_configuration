from tests.example_project.example_project.settings import INSTALLED_APPS

INSTALLED_APPS.remove(
    'mrsage.django.deployment_configuration',
)
INSTALLED_APPS.append(
    'mrsage.django.deployment_configuration.apps.DeploymentConfigurationTestConfig'
)
