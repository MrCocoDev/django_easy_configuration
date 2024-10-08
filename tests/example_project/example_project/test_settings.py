from tests.example_project.example_project.settings import *  # no-qa

try:
    INSTALLED_APPS.remove(
        'cocodev.django.deployment_configuration',
    )
except ValueError:
    ...

test_mod = 'cocodev.django.deployment_configuration.apps.DeploymentConfigurationTestConfig'
if test_mod not in INSTALLED_APPS:
    INSTALLED_APPS.insert(
        -1,
        test_mod,
    )
