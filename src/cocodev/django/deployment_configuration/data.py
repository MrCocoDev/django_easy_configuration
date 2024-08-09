import dataclasses

from cocodev.django.deployment_configuration.typing import DefaultChangeBehavior


@dataclasses.dataclass(frozen=True, kw_only=True)
class Metadata:
    documentation: str = ''
    behavior_when_default_changes: DefaultChangeBehavior = DefaultChangeBehavior.ALWAYS


Metadata.DefaultChangeBehavior = DefaultChangeBehavior
