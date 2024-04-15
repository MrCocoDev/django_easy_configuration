import dataclasses

from mrsage.django.deployment_configuration.typing import DEFAULT_BEHAVIOR_CHANGE


@dataclasses.dataclass(frozen=True, kw_only=True)
class Metadata:
    documentation: str
    behavior_when_default_changes: DEFAULT_BEHAVIOR_CHANGE
