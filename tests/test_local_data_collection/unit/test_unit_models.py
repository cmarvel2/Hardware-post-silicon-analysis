import dataclasses

import pytest
from pydantic import ValidationError

from local_data_collection.sensor_polling.models import HardwareDataStorage, HardwarePayload


def make_snapshot(**overrides):
    defaults = {
        "timestamp": "20260906_154000123",
        "hardware_name": "Intel i7 /intelcpu/0",
        "sensor_name": "CPU Core #1",
        "sensor_type": "Temperature",
        "sensor_value": 42.5,
    }
    defaults.update(overrides)
    return HardwareDataStorage(**defaults)


def test_hardware_payload_when_no_fields_given_defaults_to_empty_metadata_and_snapshots():
    payload = HardwarePayload()

    assert payload.metadata == {}
    assert payload.snapshots == []


def test_hardware_payload_when_snapshot_given_as_dict_is_coerced_to_dataclass():
    snapshot_dict = dataclasses.asdict(make_snapshot())

    payload = HardwarePayload(snapshots=[snapshot_dict])

    assert isinstance(payload.snapshots[0], HardwareDataStorage)


def test_hardware_payload_when_sensor_value_is_not_numeric_raises_validation_error():
    snapshot_dict = dataclasses.asdict(make_snapshot(sensor_value="hot"))

    with pytest.raises(ValidationError):
        HardwarePayload(snapshots=[snapshot_dict])


def test_hardware_payload_when_snapshot_instance_is_given_is_not_revalidated():
    snapshot = make_snapshot(sensor_value="hot")

    payload = HardwarePayload(snapshots=[snapshot])

    assert payload.snapshots[0].sensor_value == "hot"


def test_hardware_payload_when_dumped_and_revalidated_round_trips():
    payload = HardwarePayload(metadata={"test_id": "abc-123"}, snapshots=[make_snapshot()])

    copy = HardwarePayload.model_validate(payload.model_dump())

    assert copy == payload


def test_hardware_data_storage_when_new_attribute_assigned_raises_attribute_error():
    snapshot = make_snapshot()

    with pytest.raises(AttributeError):
        snapshot.extra_field = "not allowed by slots"