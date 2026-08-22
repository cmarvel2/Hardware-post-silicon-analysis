from local_data_collection.sensor_polling.adls_payload import UploadMemory, upload_blob, get_container
from local_data_collection.sensor_polling.models import HardwareDataStorage, HardwarePayload

def test_upload_memory_count():
    memory = UploadMemory()

    assert memory.count == 0

def test_check_buffer_below_limit():
    memory = UploadMemory()
    sensor = HardwareDataStorage(
        timestamp="20260821_004800000",
        hardware_name="Intel Core i7",
        sensor_name="CPU Package",
        sensor_type="Temperature",
        sensor_value=55.5
    )
    memory.payload.snapshots.append(sensor)

    buffer_complete = memory.check_buffer(2)

    assert buffer_complete == False

def test_check_buffer_at_limit():
    memory = UploadMemory()
    sensor = HardwareDataStorage(
        timestamp="20260821_004800000",
        hardware_name="Intel Core i7",
        sensor_name="CPU Package",
        sensor_type="Temperature",
        sensor_value=55.5
    )
    memory.payload.snapshots.append(sensor)

    buffer_complete = memory.check_buffer(1)

    assert buffer_complete == True

def test_check_buffer_above_limit():
    memory = UploadMemory()
    sensor = HardwareDataStorage(
        timestamp="20260821_004800000",
        hardware_name="Intel Core i7",
        sensor_name="CPU Package",
        sensor_type="Temperature",
        sensor_value=55.5
    )
    memory.payload.snapshots.extend([sensor, sensor])

    buffer_complete = memory.check_buffer(1)

    assert buffer_complete == True

def test_clear_buffer_uploaded():
    memory = UploadMemory()
    sensor = HardwareDataStorage(
        timestamp="20260821_004800000",
        hardware_name="Intel Core i7",
        sensor_name="CPU Package",
        sensor_type="Temperature",
        sensor_value=55.5
    )
    memory.payload.snapshots.append(sensor)

    memory.clear_buffer(True)

    assert memory.payload.snapshots == []

def test_clear_buffer_not_uploaded():
    memory = UploadMemory()
    sensor = HardwareDataStorage(
        timestamp="20260821_004800000",
        hardware_name="Intel Core i7",
        sensor_name="CPU Package",
        sensor_type="Temperature",
        sensor_value=55.5
    )
    memory.payload.snapshots.append(sensor)

    memory.clear_buffer(False)

    assert len(memory.payload.snapshots) == 1

def test_get_container_valid(monkeypatch):
    monkeypatch.setenv("CURRENT_ENVIRONMENT", "dev")
    monkeypatch.setenv("AZURE_HW_BLOB_NAME_DEV", "mock-dev-container")

    container_name = get_container()

    assert container_name == "mock-dev-container"


def test_get_container_invalid(monkeypatch):
    monkeypatch.setenv("CURRENT_ENVIRONMENT", "invalid_env")

    container_name = get_container()

    assert container_name is None

def test_upload_blob_buffer_incomplete():
    payload = HardwarePayload()

    result = upload_blob(None, None, False, payload, "mock-container")

    assert result is None

def test_upload_blob_invalid_account_url():
    payload = HardwarePayload()

    result = upload_blob(None, None, True, payload, "mock-container")

    assert result == False