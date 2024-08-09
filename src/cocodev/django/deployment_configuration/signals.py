import logging
from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from cocodev.django.deployment_configuration.django_settings_helpers import (
    LIBRARY_SETTINGS,
)
from cocodev.django.deployment_configuration.models import Option
from cocodev.django.deployment_configuration.retrieve import get_option_from_db

log = logging.getLogger(__name__)


@receiver(post_save, sender=Option, )
def surgical_cache_clear(
        sender: Type[Option],
        instance: Option,
        created: bool,
        raw: bool,
        using: str,
        update_fields,
        **kwargs,
):
    """
    Clear the cache for the deployment setting that was just updated. Immediately
    after put the new value in the cache. Doing this will avoid hitting the database
    in any code which uses deployment settings minus scenarios with a TTL.
    """
    if LIBRARY_SETTINGS.use_cache:
        log.info("Clearing cache for %s", instance.name)
        get_option_from_db.clear_cache(
            key=get_option_from_db.make_key(instance.name)
        )
        # We could avoid hitting the database again here, but we'd have to make sure we
        # exactly replicate the cache function logic. In favor of being DRY we take a slight
        # performance hit.
        get_option_from_db(instance.name)
