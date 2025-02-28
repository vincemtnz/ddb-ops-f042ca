from ddb_ops.models import PhoneNumberCapability
from ddb_ops.types import Capability


class PhoneNumberCapabilityDataService:
    def get(self, phone_number: str, channel: str) -> PhoneNumberCapability:
        return PhoneNumberCapability.get(phone_number, channel)

    def put(self, phone_number: str, channel: str, capability: Capability):
        return PhoneNumberCapability(
            phone_number, channel, capability=capability
        ).save()
