from enum import Enum


class Channel(str, Enum):
    """Supported channels."""

    RCS = "RCS"


class CapabilityCode(str, Enum):
    """Capability codes for any given phone number."""

    ENABLED = "ENABLED"
    UNREACHABLE = "UNREACHABLE"
    AGENT_NOT_LAUNCHED = "AGENT_NOT_LAUNCHED"
    REJECTED_NETWORK = "REJECTED_NETWORK"
    REJECTED_ROUTE_NOT_AVAILABLE = "REJECTED_ROUTE_NOT_AVAILABLE"
    REQUEST_FAILED = "REQUEST_FAILED"
    INVALID_DESTINATION_ADDRESS = "INVALID_DESTINATION_ADDRESS"
    UNKNOWN_CODE = "UNKNOWN_CODE"
