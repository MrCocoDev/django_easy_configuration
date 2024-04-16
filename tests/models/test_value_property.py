import pytest

from mrsage.django.deployment_configuration.models import Option, OptionType


@pytest.mark.django_db
def test_value_property_hydrates_properly():
    db_default_type = OptionType.objects.create(python_callable='builtins.list', documentation='Just for this test')
    option = Option.objects.create(
        name="UNIT_TEST",
        raw_value="[{9, 1, '55'}, {'r': 't'}, 88, 'test']",
        option_type=db_default_type,
        default_type=db_default_type,
        default_value='{0, 0}',
        default_value_change_behavior="always_change",
        documentation="Unit testing",
    )

    actual = option.value
    expected = [{9, 1, '55'}, {'r': 't'}, 88, 'test']

    assert actual == expected
