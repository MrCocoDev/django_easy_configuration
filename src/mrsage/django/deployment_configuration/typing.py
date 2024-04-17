from django.db import models
from django.utils.translation import gettext_lazy as _


class DefaultChangeBehavior(models.TextChoices):
    ALWAYS = 'always_change', _("Always Change")
    NEVER = 'never_change', _("Never Change")
    CHANGE_IF_UNCHANGED = 'change_if_unchanged', _("Change if Unchanged")
