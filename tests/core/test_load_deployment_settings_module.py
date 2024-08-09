from cocodev.django.deployment_configuration.core import load_deployment_settings_module


def test_load_deployment_settings_module_with_path(settings):
    from tests.example_project.example_project import deployment_settings

    result = load_deployment_settings_module(settings.BASE_DIR / "example_project" / 'deployment_settings.py')
    expected = deployment_settings

    assert result.__spec__.origin == expected.__spec__.origin, "Did not load the settings file correctly"


def test_load_deployment_settings_module_with_path_string(settings):
    from tests.example_project.example_project import deployment_settings

    string = str(settings.BASE_DIR / "example_project" / 'deployment_settings.py')
    result = load_deployment_settings_module(string)
    expected = deployment_settings

    assert result.__spec__.origin == expected.__spec__.origin, "Did not load the settings file correctly"


def test_load_deployment_settings_module_with_module_path():
    from tests.example_project.example_project import deployment_settings

    string = 'tests.example_project.example_project.deployment_settings'
    result = load_deployment_settings_module(string)
    expected = deployment_settings

    assert result.__spec__.origin == expected.__spec__.origin, "Did not load the settings file correctly"
