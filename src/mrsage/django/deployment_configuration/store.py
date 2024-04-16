import logging
from typing import Iterable

from mrsage.django.deployment_configuration.exceptions import InvalidTypeForOption
from mrsage.django.deployment_configuration.import_helper import callable_from_string
from mrsage.django.deployment_configuration.models import Option, OptionType
from mrsage.django.deployment_configuration.typing import DEFAULT_BEHAVIOR_CHANGE

log = logging.getLogger(__name__)


def push_data_to_database(
        *,
        option_name: str,
        default_value: str,
        default_type: str,
        supported_types: Iterable[str],
        default_behavior: DEFAULT_BEHAVIOR_CHANGE,
        help_string: str,
):
    """
    Pushes the deployment option into the database and creates the related
    models.

    Args:
        option_name:
        default_value:
        default_type:
        supported_types:
        default_behavior:
        help_string:

    Returns:

    """
    # Validate some things
    if default_type not in supported_types:
        raise InvalidTypeForOption(
            f"Invalid type: {option_name} supports {supported_types} but "
            f"has a default of {default_type}"
        )

    db_default_type, _ = generate_option_type(default_type)
    db_supported_types = [generate_option_type(supported_type)[0] for supported_type in supported_types]

    option: Option = Option.objects.filter(name=option_name).first()
    if not option:
        # Option does not exist yet
        option = Option.objects.create(
            name=option_name,
            raw_value=default_value,
            option_type=db_default_type,
            default_type=db_default_type,
            default_value=default_value,
            default_value_change_behavior=default_behavior,
            documentation=help_string,
        )
        option.supported_types.add(*db_supported_types)
    else:
        # Option exists

        # Update the default behavior first
        option.default_value_change_behavior = default_behavior

        # If the value always changes with the default
        if option.default_value_change_behavior == Option.DefaultChangeBehavior.ALWAYS:
            option.raw_value = default_value
            option.option_type = db_default_type

        # If the value changes if it is still the old default
        if (
                option.default_value_change_behavior == Option.DefaultChangeBehavior.CHANGE_IF_UNCHANGED
                and option.raw_value == option.default_value
        ):
            option.raw_value = default_value
            option.option_type = db_default_type

        # Error correction
        if option.option_type.python_callable not in supported_types:
            log.error(
                "Configuration option's supported types were changed "
                "and do not include the existing type, resetting to default",
                extra={
                    'data': {
                        'option': option.name,
                        'old_value': option.raw_value,
                        'old_type': option.option_type,
                        'new_value': default_value,
                        'new_type': default_type,
                    }
                }
            )
            option.raw_value = default_value
            option.option_type = default_type

        option.default_value = default_value
        option.default_type = db_default_type
        option.documentation = help_string

        option.save()
        option.supported_types.add(*db_supported_types)

    return option


def generate_option_type(default_type) -> tuple[OptionType, bool]:
    return OptionType.objects.update_or_create(
        python_callable=default_type,
        defaults={
            'documentation': callable_from_string(default_type).__doc__
        }
    )


def clean_up_old_options(existing_options: Iterable[str]):
    old_options = Option.objects.exclude(name__in=existing_options)
    if old_options:
        log.warning("Deleting old options: %s", old_options.values_list('name', flat=True))

    return old_options.delete()
