import os
from datetime import datetime, timezone
from typing import override

from dotenv import load_dotenv
from pynamodb.attributes import Attribute, BooleanAttribute, UnicodeAttribute
from pynamodb.constants import STRING
from pynamodb.models import Model

from ddb_ops.types import CapabilityCode

# Load environment variables from .env file, if present.
# We're mainly using
load_dotenv()

from rich.console import Console

console = Console()


class CapabilityAttribute(Attribute[CapabilityCode]):
    attr_type = STRING

    @override
    def serialize(self, value: CapabilityCode) -> str:
        console.log("serialize called:", value)
        return value.value

    @override
    def deserialize(self, value: str) -> CapabilityCode:
        console.log("deserialize called:", value)
        return CapabilityCode(value)


class PhoneNumberCapability(Model):
    class Meta:
        table_name = os.environ.get("TABLE_NAME", "phone_number_capabilities")

    phone_number = UnicodeAttribute(hash_key=True)
    channel = UnicodeAttribute(range_key=True)
    is_capable = BooleanAttribute(default=True)
    last_refreshed_at = UnicodeAttribute(
        default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    capability = CapabilityAttribute(null=True)
