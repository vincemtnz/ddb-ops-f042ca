"""PhoneNumberCapability model."""

from __future__ import annotations

import typing
from datetime import datetime

from pynamodb.attributes import Attribute, UnicodeAttribute
from pynamodb.constants import STRING
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model

from ..types import Channel, CapabilityCode
from .. import constants


class LastUpdatedAtIndex(GlobalSecondaryIndex["PhoneNumberCapability"]):
    """LastUpdatedAtIndex GSI definition.

    Attributes
    ----------
        last_refreshed_at(hash_key)
        channel(range_key)

    """

    class Meta:  # noqa: D106
        index_name = constants.LAST_REFRESHED_AT_INDEX_NAME
        projection = AllProjection()
        billing_mode = "PAY_PER_REQUEST"

    last_refreshed_at = UnicodeAttribute(hash_key=True, null=False)
    channel = UnicodeAttribute(range_key=True, null=False)


class CapabilityStatusAttribute(Attribute[CapabilityCode]):
    """Custom attribute for CapabilityStatus."""

    attr_type = STRING
    """Attribute type."""

    def serialize(self, capability_code: CapabilityCode) -> str:
        """Serialize CapabilityCode to string."""
        if not isinstance(capability_code, CapabilityCode):
            raise ValueError(f"Expected CapabilityCode, got {type(capability_code)}")
        return capability_code.value

    def deserialize(self, value: str) -> CapabilityCode:
        """Deserialize string to CapabilityCode."""
        return CapabilityCode(value)


class PhoneNumberCapability(Model):
    """PhoneNumberCapability model definition.

    Attributes
    ----------
        phone_number: The phone number.
        channel: The channel (e.g. RCS).
        is_capable: The capability status.
        last_refreshed_at: The last refreshed date (YYYY-MM-DD). Defaults to the current date.

    """

    class Meta:  # noqa: D106
        table_name = constants.TABLE_NAME
        region = constants.TABLE_REGION
        billing_mode = "PAY_PER_REQUEST"

    phone_number = UnicodeAttribute(hash_key=True, null=False)
    channel = UnicodeAttribute(range_key=True, default=Channel.RCS.value, null=False)
    last_refreshed_at = UnicodeAttribute(
        default=lambda: datetime.now().strftime("%Y-%m-%d"), null=False
    )
    last_refreshed_at_index = LastUpdatedAtIndex()
    capability_status = CapabilityStatusAttribute(null=False)

    @property
    def is_capable(self) -> bool:
        """Check if the phone number is capable."""
        return self.capability_status == CapabilityCode.ENABLED

    def __eq__(self, other: typing.Any) -> bool:
        """Equality comparison between two PhoneNumberCapability objects."""
        if not isinstance(other, PhoneNumberCapability):
            return False
        return bool(self.serialize() == other.serialize())
