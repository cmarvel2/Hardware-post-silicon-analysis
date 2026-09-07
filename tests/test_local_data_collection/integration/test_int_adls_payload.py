import os

import pytest
from azure.identity import ClientSecretCredential
from dotenv import find_dotenv, load_dotenv

from local_data_collection.sensor_polling.adls_payload import adls_credentials, upload_blob
from local_data_collection.sensor_polling.models import HardwareDataStorage, HardwarePayload

load_dotenv(find_dotenv())

REQUIRED_TEST_ENV_VARS = (
    "AZURE_CLIENT_ID",
    "AZURE_TENANT_ID",
    "AZURE_CLIENT_SECRET",
    "TEST_LANDING_CONTAINER",
    "TEST_AZURE_STORAGE_URL",
)

UNREACHABLE_ENV_MAPPING = {
    "CONTAINER": "landing",
    "STORAGE_URL": "https://127.0.0.1:1/",
}


def require_test_environment():
    missing = [var for var in REQUIRED_TEST_ENV_VARS if not os.getenv(var)]
    if missing:
        raise AssertionError(
            f"Missing test-environment variables (expected in .env or shell): {', '.join(missing)}"
        )


def make_payload(test_id="int-test-123"):
    snapshot = HardwareDataStorage(
        timestamp="20260906_154000123",
        hardware_name="Integration Test Hardware /test/0",
        sensor_name="Integration Sensor",
        sensor_type="Temperature",
        sensor_value=42.5,
    )
    return HardwarePayload(metadata={"test_id": test_id}, snapshots=[snapshot])


def dummy_credentials():
    return ClientSecretCredential(client_id="id", client_secret="secret", tenant_id="tenant")


def test_upload_blob_when_storage_account_is_unreachable_returns_false():
    result = upload_blob(
        credentials=dummy_credentials(),
        env_mapping=UNREACHABLE_ENV_MAPPING,
        sensor_buffer=make_payload(),
    )

    assert result is False


def test_upload_blob_when_payload_fails_validation_returns_false():
    sensor_buffer = HardwarePayload(metadata={"test_id": "invalid-payload"})
    sensor_buffer.snapshots.append(
        HardwareDataStorage(
            timestamp="20260906_154000123",
            hardware_name="hw",
            sensor_name="sensor",
            sensor_type="Temperature",
            sensor_value="not-a-number",
        )
    )

    with pytest.warns(UserWarning, match="PydanticSerializationUnexpectedValue"):
        result = upload_blob(
            credentials=dummy_credentials(),
            env_mapping=UNREACHABLE_ENV_MAPPING,
            sensor_buffer=sensor_buffer,
        )

    assert result is False


def test_upload_blob_when_payload_and_credentials_are_valid_returns_true():
    require_test_environment()

    credentials, env_mapping = adls_credentials("test")

    result = upload_blob(
        credentials=credentials,
        env_mapping=env_mapping,
        sensor_buffer=make_payload(),
    )

    assert result is True, (
        "upload_blob returned False — check that the service principal has Storage Blob Data "
        "Contributor on the TEST landing container and that the .env values are correct"
    )