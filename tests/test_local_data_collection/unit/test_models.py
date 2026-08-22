from local_data_collection.sensor_polling.models import HardwareDataStorage, HardwarePayload

def test_hardware_data_storage():
    sensor = HardwareDataStorage(
        timestamp="20260821_004800000",
        hardware_name="Intel Core i7",
        sensor_name="CPU Package",
        sensor_type="Temperature",
        sensor_value=55.5
    )

    assert sensor.sensor_value == 55.5

def test_hardware_data_storage_none_values():
    sensor = HardwareDataStorage(
        timestamp=None,
        hardware_name=None,
        sensor_name=None,
        sensor_type=None,
        sensor_value=None
    )

    assert sensor.sensor_value is None

def test_hardware_payload_default_metadata():
    payload = HardwarePayload()

    assert payload.metadata == {}

def test_hardware_payload_default_snapshots():
    payload = HardwarePayload()

    assert payload.snapshots == []