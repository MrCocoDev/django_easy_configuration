from cocodev.django.deployment_configuration.import_helper import import_from_filepath


def test_loads_file_correctly(settings):
    from tests.example_project.example_project import deployment_settings

    result = import_from_filepath(settings.BASE_DIR / "example_project" / 'deployment_settings.py')
    expected = deployment_settings

    assert result.__spec__.origin == expected.__spec__.origin, "Did not load the settings file correctly"
