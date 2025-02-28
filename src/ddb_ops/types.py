from enum import Enum
from typing import Literal

Capability = Literal["ENABLED", "UNREACHABLE", "UNKNOWN"]


class CapabilityCode(str, Enum):
    ENABLED = "ENABLED"
    UNREACHABLE = "UNREACHABLE"
    UNKNOWN = "UNKNOWN"
