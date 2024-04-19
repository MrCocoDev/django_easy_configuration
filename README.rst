.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/MrSage/django-easy-configuration.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/MrSage/django-easy-configuration
    .. image:: https://readthedocs.org/projects/django-easy-configuration/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://django-easy-configuration.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/MrSage/django-easy-configuration/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/MrSage/django-easy-configuration
    .. image:: https://img.shields.io/pypi/v/django-easy-configuration.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/django-easy-configuration/
    .. image:: https://img.shields.io/conda/vn/conda-forge/django-easy-configuration.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/django-easy-configuration
    .. image:: https://pepy.tech/badge/django-easy-configuration/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/django-easy-configuration
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/django-easy-configuration

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===============================
django-easy-configuration
===============================


    Quick and easy configuration of a deployment through Django Admin!


For some Django projects there are configuration or customer specific variables that need
to be toggled and tweaked. You might be using env files, variables, or other technologies
which often need a server restart to take effect. Sometimes this variables get encapsulated
into DB tables, but sometimes they don't fit so well. This library seeks to make this kind
of configuration brainlessly easy.


Getting Started
---------------

Create a file somewhere in your project, you may name it anything you like. For the purposes
of the README we will call it `deployment_settings.py`:

::

    # my.modules.deployment_settings.py
    CUSTOMER_DISPLAY_NAME: str = "Example Customer"
    NETWORK_TIMEOUT: float = 10.0

And then configure the library in your django settings file:

::

    # settings.py
    DEPLOYMENT_CONFIGURATION_SETTINGS = {
        'deployment_settings_file': 'my.modules.deployment_settings',
    }

Now, boot up your server and head to the Admin panel. You should see **Option**s and **OptionType**s
in the sidebar. If you inspect them you will see that **builtins.str** and **builtins.float** have
automatically been added to the database, as you adjust your deployment_settings file you will see
these automatically change. You should never need to interact with these directly.

If you look at **Option**s you will see there are two option loaded into the database:
*CUSTOMER_DISPLAY_NAME*, and *NETWORK_TIMEOUT*. For the basic examples shown above you won't be able to
configure much about these options except for to modify their values. If we use a more advanced
setup there will be more options to explore:

::

    # my.modules.deployment_settings.py
    from typing import Annotated
    from mrsage.django.deployment_configuration.typing import Metadata

    CUSTOMER_DISPLAY_NAME: Annotated[
        str,
        Metadata(
            documentation=(
                "<h1>How to use the Customer Display Name<h1><p>This field controls the display "
                "value of the brand name on the customer's site. It is important that this field is "
                "accurate and up-to-date with the customer's branding. "
            ),
            behavior_when_default_changes=Metadata.DefaultChangeBehavior.NEVER,
        )
    ] = "Example Customer"
    NETWORK_TIMEOUT: Annotated[
        int | float,
        Metadata(documentation="Set this higher for customers with high latency networks"),
    ] = 10.0

Now if you load up the Django admin again you'll see that the documentation for each variable is
rendered as HTML, making it easy to provide detailed information to your Technical Account Manager's
and other non-engineers who may be making these changes. When you look at **NETWORK_TIMEOUT** you can
see that you can change the type as well as the value. This library adds native support for all the
builtin types, *but currently does not have special UX for array-like types*.

Using With Python
-----------------

To use this library inside of your codebase just import your module as normal and everything should
**Just Work™**.

::

    # some.other.module
    import httpx
    from my.modules import deployment_settings

    def do_something():
        return httpx.post(..., timeout=deployment_settings.NETWORK_TIMEOUT)

Possible Issues
---------------

Unfortunately, things rarely ever **Just Work™**. There are some considerations to take into account
when using this library:

- Caching: This library uses the Django cache system to prevent database lookups when your code accesses
the configuration variables. If your cache is not setup properly then every variable lookup will incur a
database lookup. This will potentially impact load times and site stability!


.. _pyscaffold-notes:

Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd django-easy-configuration
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
