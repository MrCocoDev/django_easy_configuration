from typing import Annotated

from mrsage.django.deployment_configuration.data import Metadata

VAR_A: Annotated[
    int | str | set,  # Allowed types
    Metadata(
        documentation="This is a basic example of deployment configuration",
        behavior_when_default_changes="never_change",
    )
] = 99  # Default value and type
