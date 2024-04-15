"""
    Dummy conftest.py for deployment_configuration.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest


@pytest.fixture()
def deployment_settings_module():
    """
    Convenience fixture to access the deployment settings module in the
    example project
    """
    import tests.example_project.example_project.deployment_settings
    return tests.example_project.example_project.deployment_settings
