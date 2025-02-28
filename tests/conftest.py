import pytest
import os

# Ensure the environment has the necessary env vars
@pytest.fixture(autouse=True)
def setup_env():
    os.environ.setdefault('TABLE_NAME', 'phone_number_capabilities_test')
    yield
