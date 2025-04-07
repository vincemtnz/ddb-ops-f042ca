import os

import pytest
from datetime import datetime
from moto import mock_aws
from rich import print

from ddb_ops.models.phone_number_capability import PhoneNumberCapability
from ddb_ops.tasks.seed import run_seed


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


def test_seed_task():
    run_seed(
        total=10,
        date=datetime.now().strftime("%Y-%d-%m"),
        prefix="PYTEST",
        execute=True,
    )

    records = [record for record in PhoneNumberCapability.scan()]

    assert len(records) == 10
