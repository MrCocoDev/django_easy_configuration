import importlib
import importlib.util


def callable_from_string(callable_string):
    module_str, attr_name = callable_string.rsplit('.', maxsplit=1)
    module = importlib.import_module(module_str)
    return getattr(module, attr_name)


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
