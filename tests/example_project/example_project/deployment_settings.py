import dataclasses
from typing import Annotated

from mrsage.django.deployment_configuration.typing import DEFAULT_BEHAVIOR_CHANGE


@dataclasses.dataclass(frozen=True, kw_only=True)
class Metadata:
    documentation: str
    behavior_when_default_changes: DEFAULT_BEHAVIOR_CHANGE


VAR_A: Annotated[
    int | str | set,  # Allowed types
    Metadata(
        documentation="This is a basic example of deployment configuration",
        behavior_when_default_changes="never_change",
    )
] = 99  # Default value and type
