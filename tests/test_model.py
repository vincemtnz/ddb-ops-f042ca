import os
from datetime import datetime, timezone

import pytest
from moto import mock_aws
from rich.console import Console

from ddb_ops.models.phone_number_capability import PhoneNumberCapability
from ddb_ops.types import CapabilityCode

console = Console()


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def mocked_aws(aws_credentials):
    with mock_aws(config={"core": {"service_whitelist": ["dynamodb"]}}):
        yield


@pytest.fixture(scope="function", autouse=True)
def setup_table(mocked_aws):
    PhoneNumberCapability.create_table()
    yield
    PhoneNumberCapability.delete_table()


def test_default_values_on_new_items():
    PhoneNumberCapability(phone_number="1234567890", channel="rcs").save()  # pyright: ignore[reportUnusedCallResult]

    result = PhoneNumberCapability.get("1234567890", "rcs")

    assert result.attribute_values == {
        "phone_number": "1234567890",
        "channel": "rcs",
        "is_capable": True,
        "last_refreshed_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


def test_capability_code_serde():
    PhoneNumberCapability(
        phone_number="1234567890", channel="rcs", capability=CapabilityCode.ENABLED
    ).save()  # pyright: ignore[reportUnusedCallResult]

    result = PhoneNumberCapability.get("1234567890", "rcs")

    assert result.capability == CapabilityCode.ENABLED
    assert isinstance(result.capability, CapabilityCode)
    assert result.attribute_values == {
        "phone_number": "1234567890",
        "channel": "rcs",
        "is_capable": True,
        "last_refreshed_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "capability": "ENABLED",
    }
