import importlib


def callable_from_string(callable_string):
    module_str, attr_name = callable_string.rsplit('.', maxsplit=1)
    module = importlib.import_module(module_str)
    return getattr(module, attr_name)
