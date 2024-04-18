"""
Where the fun stuff happens
"""
import ast
import importlib
import logging
import typing
from functools import singledispatch
from pathlib import Path
from types import ModuleType

import django.db.utils

from mrsage.django.deployment_configuration.data import Metadata
from mrsage.django.deployment_configuration.import_helper import (
    callable_from_string,
    import_from_filepath,
)
from mrsage.django.deployment_configuration.metadata import _APP

log = logging.getLogger(__name__)

HYDRATION_MAP: typing.Annotated[
    dict[str, typing.Callable],
    """
    This is required to make the builtin functions work off string values. Maybe
    there is another way to sneakily slide these callables over top of the base
    callable, but this works well enough. For your own callables, make sure that they
    can accept a string and return a value.
    """
] = {
    'builtins.list': lambda v: list(ast.literal_eval(v)),
    'builtins.set': lambda v: set() if v == "{}" else set(ast.literal_eval(v)) ,
    'builtins.dict': lambda v: dict(ast.literal_eval(v)),
    'builtins.NoneType': lambda v: None,
}


def load_deployment_settings_module(file_or_module_path: Path | str, /) -> ModuleType:
    """
    Loads the deployment settings module from a string or Path. This
    is how we transform the settings value into the actual python it
    refers to.

    Args:
        file_or_module_path: A string, filepath, or module path to load
            as a python module

    Returns: The python module represented by the input string
    """
    try:
        if isinstance(file_or_module_path, Path) or Path(file_or_module_path).exists():
            _APP['loaded'] = 'file'
            return import_from_filepath(file_or_module_path)

    except TypeError:
        ...

    _APP['loaded'] = 'module'
    return importlib.import_module(file_or_module_path)


def generate_type_string_from_variable(variable) -> str:
    """
    Accepts a variable returns an importable module string
    """
    the_type = type(variable)
    return generate_type_string_from_type(the_type)


def find_metadata(variable_type) -> typing.Optional[Metadata]:
    """
    Searches through the annotated metadata for our Metadata class
    """
    if hasattr(variable_type, "__metadata__"):
        for value in variable_type.__metadata__:
            if isinstance(value, Metadata):
                return value


def generate_type_string_from_type(the_type):
    """
    Generates a callable string from a type.

    Example:
        >>> assert generate_type_string_from_type(str) == "builtins.str"

    Args:
        the_type: Any type that can be used within this library

    Returns: A callable string for use within this library
    """
    type_name = the_type.__qualname__
    module = the_type.__module__
    return f"{module}.{type_name}"


def generate_deployment_settings_safely(deployment_settings_module: ModuleType):
    try:
        generate_deployment_settings(deployment_settings_module)
    except django.db.utils.OperationalError:
        # Probably migrations
        log.error(
            "Could not create deployment settings in database! "
            "If you're running migrations you can safely ignore this."
        )


def generate_deployment_settings(deployment_settings_module: ModuleType):
    """
    Iterates over the deployment settings file and generates the necessary
    data in the database.
    """
    # This function runs once, so we pay for the local import instead of paying
    # every time a value is accessed
    from mrsage.django.deployment_configuration.store import (
        clean_up_old_options,
        push_data_to_database,
    )

    for variable_name, variable_type in deployment_settings_module.__annotations__.items():
        default_value = getattr(deployment_settings_module, variable_name)
        default_type = generate_type_string_from_variable(default_value)
        metadata = find_metadata(variable_type) or Metadata()

        if type_args := typing.get_args(variable_type):
            raw_supported_types = type_args[0]
            supported_types = {
                generate_type_string_from_type(supported_type)
                for supported_type
                in typing.get_args(raw_supported_types)
            }
        else:
            supported_types = {
                generate_type_string_from_type(variable_type)
            }

        push_data_to_database(
            option_name=variable_name,
            default_value=default_value,
            default_type=default_type,
            supported_types=supported_types,
            default_behavior=metadata.behavior_when_default_changes,
            help_string=metadata.documentation,
        )

    all_deployment_option_names = deployment_settings_module.__annotations__.keys()
    clean_up_old_options(all_deployment_option_names)


def hydrate_value(value, callable_str):
    """
    Converts a value and a callable string into the value returned
    by the callable when passed the value.

    TODO allow registering a function for a callable to allow for customization

    Args:
        value: The input to the callable represented by the string
        callable_str: A string which represents a callable (ex: builtins.str)

    Returns: The converted value of the input
    """
    actual_callable = HYDRATION_MAP.get(
        callable_str,
        callable_from_string(callable_str),
    )
    return actual_callable(value)


@singledispatch
def dehydrate_value(new_value: typing.Any) -> str:
    """
    Serializes the value into a string. Register a function with a type to
    customize the serialization.
    """
    return str(new_value)
