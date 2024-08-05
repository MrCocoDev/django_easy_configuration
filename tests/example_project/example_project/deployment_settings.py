from typing import Annotated

from mrsage.django.deployment_configuration.data import Metadata
from mrsage.django.deployment_configuration.typing import DefaultChangeBehavior

VAR_A: Annotated[
    int | str | set,  # Allowed types
    Metadata(
        documentation="This is a <em>basic example</em> of deployment configuration",
        behavior_when_default_changes=DefaultChangeBehavior.NEVER,
    )
] = 99  # Default value and type
VAR_B: float = 99.12321
