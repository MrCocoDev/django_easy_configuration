import random

import pytest

from cocodev.django.deployment_configuration.models import Option


@pytest.mark.django_db
def test_retrieval(deployment_settings_module, django_assert_num_queries):
    ds = deployment_settings_module

    # Assure ourselves that we have an uncontaminated environment
    from cocodev.django.deployment_configuration import magic
    assert magic.MAGICKED_MODULE is None, "Deployment settings wasn't replaced"

    # Fully load the library, replacing the module in place
    from cocodev.django.deployment_configuration.load import fully_load_library
    fully_load_library()
    assert magic.MAGICKED_MODULE == ds, "Deployment settings wasn't replaced"

    # Create a random value to test with (this can be improved with hypothesis)
    expected = random.randint(-1000, 1000)
    for x in ('VAR_A', 'VAR_B'):
        var = Option.objects.filter(name=x).first()
        var.raw_value = str(expected)
        var.save()

    with django_assert_num_queries(0):
        # No queries are made because the values have already been loaded into the cache

        # Check that the random value was retrieved
        assert ds.VAR_B == expected, "VAR_B was not retrieved correctly"
        assert ds.VAR_A == expected, "VAR_A was not retrieved correctly"
