from django.db import models


def meta_fields() -> tuple[models.DateTimeField, models.DateTimeField]:
    """
    Convenience for creating consistent db metadata columns.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    return created_at, updated_at


class Option(models.Model):

    class DefaultChangeBehavior(models.TextChoices):
        ALWAYS = "always"
        NEVER = "never"
        CHANGE_IF_UNCHANGED = "change_if_unchanged"

    created, updated = meta_fields()

    name = models.CharField(max_length=2048)
    value = models.CharField(max_length=2048)
    option_type = models.ForeignKey(to='OptionType', on_delete=models.PROTECT)

    supported_types = models.ManyToManyField(to='OptionType', related_name='supportedoptiontypes')

    default_value = models.CharField(max_length=2048)
    default_type = models.ForeignKey(
        to='OptionType',
        on_delete=models.PROTECT,
        related_name='defaultoptiontype',
    )
    default_value_change_behavior = models.CharField(max_length=2048, choices=DefaultChangeBehavior.choices)

    documentation = models.TextField()


class OptionType(models.Model):
    created, updated = meta_fields()

    python_callable = models.CharField(max_length=2048)

    documentation = models.TextField()
