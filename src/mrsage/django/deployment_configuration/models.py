from django.db import models

from mrsage.django.deployment_configuration.core import (
    dehydrate_value,
    generate_type_string_from_type,
    hydrate_value,
)
from mrsage.django.deployment_configuration.typing import DefaultChangeBehavior


def meta_fields() -> tuple[models.DateTimeField, models.DateTimeField]:
    """
    Convenience for creating consistent db metadata columns.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    return created_at, updated_at


class Option(models.Model):
    created, updated = meta_fields()

    DefaultChangeBehavior = DefaultChangeBehavior

    name = models.CharField(max_length=2048)
    raw_value = models.CharField(max_length=2048)
    option_type = models.ForeignKey(to='OptionType', on_delete=models.PROTECT)

    supported_types = models.ManyToManyField(to='OptionType', related_name='supportedoptions')

    default_value = models.CharField(max_length=2048)
    default_type = models.ForeignKey(
        to='OptionType',
        on_delete=models.PROTECT,
        related_name='defaultoptiontype',
    )
    default_value_change_behavior = models.CharField(
        max_length=2048,
        choices=DefaultChangeBehavior.choices,
        blank=False,
        default=DefaultChangeBehavior.ALWAYS,
    )

    documentation = models.TextField()

    @property
    def value(self):
        """
        Returns the hydrated value from the database.
        """
        return hydrate_value(self.raw_value, self.option_type.python_callable)

    @value.setter
    def value(self, new_value):
        from mrsage.django.deployment_configuration.store import generate_option_type

        new_option_type_str = generate_type_string_from_type(type(new_value))
        new_option_type = generate_option_type(new_option_type_str)

        if new_option_type.pk not in self.supported_types.all().only('pk'):
            raise ValueError(
                f"Cannot assign {new_value} of type {type(new_value)} to {self.name}! "
                f"Supported types are {self.supported_types.all().values_list('python_callable', flat=True)}"
            )

        self.raw_value = dehydrate_value(new_value)
        self.option_type = new_option_type

    def reset_to_default(self):
        self.raw_value = self.default_value
        self.option_type = self.default_type

    def __str__(self):
        return self.name


class OptionType(models.Model):
    created, updated = meta_fields()

    python_callable = models.CharField(max_length=2048)

    documentation = models.TextField()

    def admin_label(self):
        return self.python_callable

    def to_callable(self):
        return
