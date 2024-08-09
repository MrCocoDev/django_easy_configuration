__all__ = ["async_deployment_settings"]

from typing import Coroutine

from asgiref.sync import sync_to_async

from cocodev.django.deployment_configuration.shortcuts import module_from_library_settings


class _AsyncDeploymentSettings:
    def __getattr__(self, item) -> Coroutine:
        return self.get_deployment_setting(item)

    def get_deployment_setting(self, name):
        return getattr(module_from_library_settings(), name)


async_deployment_settings = _AsyncDeploymentSettings()
