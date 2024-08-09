import pytest

from cocodev.django.deployment_configuration.store import push_data_to_database


@pytest.mark.django_db
def test_push_data_to_database_works_on_happy_path():
    option = push_data_to_database(
        option_name="TEST_VAR",
        default_value="Hello, World!",
        default_type="builtins.str",
        supported_types=["builtins.str", "builtins.float"],
        default_behavior="always_change",
        help_string="This is a test value",
    )

    assert option.name == 'TEST_VAR'
    assert option.raw_value == option.default_value == 'Hello, World!'
    assert option.option_type.python_callable == option.default_type.python_callable == 'builtins.str'
    assert list(option.supported_types.all().values_list('python_callable', flat=True)) == ["builtins.str", "builtins.float"]
    assert option.default_value_change_behavior == 'always_change'
    assert option.documentation == "This is a test value"
