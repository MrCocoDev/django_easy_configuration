import pytest

from mrsage.django.deployment_configuration.core import (
    generate_deployment_settings_safely,
)
from mrsage.django.deployment_configuration.models import Option


@pytest.mark.django_db
def test_generate_deployment_settings(deployment_settings_module):
    generate_deployment_settings_safely(deployment_settings_module)
    option = Option.objects.filter(name='VAR_A').first()

    assert option.name == 'VAR_A'
    assert option.raw_value == option.default_value == '99'
    assert option.option_type.python_callable == option.default_type.python_callable == 'builtins.int'
    assert set(
        option.supported_types.all().values_list('python_callable', flat=True)
    ) == {"builtins.str", "builtins.int", "builtins.set"}
    assert option.default_value_change_behavior == 'never_change'
    assert option.documentation == "This is a <em>basic example</em> of deployment configuration"
