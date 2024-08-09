"""
    Dummy conftest.py for deployment_configuration.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

from importlib import reload

import pytest

from cocodev.django.deployment_configuration import magic
from cocodev.django.deployment_configuration.shortcuts import module_from_library_settings


@pytest.fixture()
def deployment_settings_module():
    """
    Convenience fixture to access the deployment settings module in the
    example project
    """
    import tests.example_project.example_project.deployment_settings
    return tests.example_project.example_project.deployment_settings


@pytest.fixture(autouse=True)
def refresh_deployment_settings_module():
    """
    If a test calls `fully_load_library` then the deployment settings file will
    always be magicked, which can cause cross-contamination with other test cases.
    This can be alleviated with the use of `pytest-random-order`, but it can still
    fly under the radar long enough for the faulty commit to be hidden in the history.
    """
    deployment_settings_module = module_from_library_settings()
    yield
    reload(deployment_settings_module)
    magic.MAGICKED_MODULE = None
