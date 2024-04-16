from django.core.exceptions import ImproperlyConfigured


class BaseDjangoDeploymentConfigurationException(Exception):
    """
    Convenience for catching all library errors.
    """
    ...


class InvalidTypeForOption(BaseDjangoDeploymentConfigurationException):
    """
    An Option was saved with a type that it does not support.
    """
    ...


class LibraryIsImproperlyConfigured(ImproperlyConfigured, BaseDjangoDeploymentConfigurationException):
    """
    Oopsies, you didn't follow the instructions!
    """
