import asyncio
import random

import pytest

from mrsage.django.deployment_configuration.load import fully_load_library
from mrsage.django.deployment_configuration.models import Option
from mrsage.django.deployment_configuration.shortcuts import module_from_library_settings


@pytest.mark.django_db
def test_some_asyncio_code():
    fully_load_library()

    # Create a random value to test with (this can be improved with hypothesis)
    expected = random.randint(-1000, 1000)
    for x in ('VAR_A', 'VAR_B'):
        var = Option.objects.filter(name=x).first()
        var.raw_value = str(expected)
        var.save()

    # Show that access from an async context works as long as caching is set up correctly
    async def testing():
        ds = module_from_library_settings()
        assert ds.VAR_B == expected

    asyncio.run(testing())
