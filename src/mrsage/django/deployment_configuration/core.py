"""
Where the fun stuff happens
"""
import importlib
import typing
from pathlib import Path
from types import ModuleType

from example_project.example_project.deployment_settings import Metadata

from mrsage.django.deployment_configuration.store import push_data_to_database


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
    if isinstance(file_or_module_path, Path) or Path(file_or_module_path).exists():
        return import_from_filepath(file_or_module_path)
    else:
        return importlib.import_module(file_or_module_path)


def import_from_filepath(filepath):
    """
    Copied from https://stackoverflow.com/a/67692

    Dynamically load a filepath as a python module and insert it into the
    system modules.

    Args:
        filepath: A string or filepath to load as a python module

    Returns: The python module represented by the input string
    """
    import importlib.util
    import sys
    module_name = "mrsage.django.deployment_configuration.tmp.deployment_settings"
    spec = importlib.util.spec_from_file_location(
        module_name,
        filepath,
    )
    foo = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = foo
    spec.loader.exec_module(foo)

    return foo


def generate_type_string_from_variable(variable) -> str:
    """
    Accepts a variable returns an importable module string
    """
    the_type = type(variable)
    return generate_type_string_from_type(the_type)


def find_metadata(variable_type):
    """
    Searches through the annotated metadata for our Metadata class
    """
    for value in variable_type.__metadata__:
        if isinstance(value, Metadata):
            return value


def generate_type_string_from_type(the_type):
    type_name = the_type.__qualname__
    module = the_type.__module__
    return f"{module}.{type_name}"


def generate_deployment_settings(deployment_settings_module: ModuleType):
    """
    {
        'VAR_A': typing.Annotated[
            int | str | set,
            Metadata(
                documentation='This is a basic example of deployment configuration',
                behavior_when_default_changes='never_change',
            )
        ]
    }
    """
    for variable_name, variable_type in deployment_settings_module.__annotations__.items():
        default_value = getattr(deployment_settings_module, variable_name)
        default_type = generate_type_string_from_variable(default_value)
        metadata = find_metadata(variable_type)
        raw_supported_types = typing.get_args(variable_type)[0]
        supported_types = {
            generate_type_string_from_type(supported_type)
            for supported_type
            in typing.get_args(raw_supported_types)
        }

        push_data_to_database(
            option_name=variable_name,
            default_value=default_value,
            default_type=default_type,
            supported_types=supported_types,
            default_behavior=metadata.behavior_when_default_changes,
            help_string=metadata.documentation,
        )
