import re

import pytest

pytest.importorskip("clr")

from local_data_collection.sensor_polling import hardware_sensor_collectors as collectors
from local_data_collection.sensor_polling.models import HardwareDataStorage

@pytest.fixture
def open_computer():
    computer, hardware_type = collectors.init_computer(cpu=True, motherboard=True, gpu=True, memory=True)
    yield computer, hardware_type
    computer.Close()


@pytest.fixture
def bare_computer():
    computer, hardware_type = collectors.init_computer()
    yield computer, hardware_type
    computer.Close()


@pytest.mark.parametrize(
    ("flag", "net_property"),
    [
        ("cpu", "IsCpuEnabled"),
        ("motherboard", "IsMotherboardEnabled"),
        ("gpu", "IsGpuEnabled"),
        ("memory", "IsMemoryEnabled"),
    ],
    ids=["cpu", "motherboard", "gpu", "memory"],
)
def test_init_computer_when_flag_is_true_sets_matching_net_property(flag, net_property):
    computer, _ = collectors.init_computer(**{flag: True})

    assert getattr(computer, net_property) is True


def test_init_computer_when_no_flags_set_leaves_all_hardware_disabled(bare_computer):
    computer, _ = bare_computer

    assert not (
        computer.IsCpuEnabled
        or computer.IsMotherboardEnabled
        or computer.IsGpuEnabled
        or computer.IsMemoryEnabled
    )


def test_init_computer_returns_hardware_type_enum(open_computer):
    _, hardware_type = open_computer

    assert hardware_type is collectors.HardwareType


def test_get_cpu_data_when_cpu_present_returns_hardware_data_storage_snapshots(open_computer):
    computer, hardware_type = open_computer

    snapshots = collectors.get_cpu_data(computer, hardware_type)

    assert len(snapshots) > 0
    assert all(isinstance(snapshot, HardwareDataStorage) for snapshot in snapshots)


def test_get_cpu_data_when_cpu_disabled_returns_empty_list(bare_computer):
    computer, hardware_type = bare_computer

    assert collectors.get_cpu_data(computer, hardware_type) == []


def test_get_cpu_data_formats_timestamp_as_utc_datetime_with_milliseconds(open_computer):
    computer, hardware_type = open_computer

    snapshots = collectors.get_cpu_data(computer, hardware_type)

    assert re.fullmatch(r"\d{8}_\d{9}", snapshots[0].timestamp)


def test_get_memory_data_when_memory_present_returns_populated_snapshots(open_computer):
    computer, hardware_type = open_computer

    snapshots = collectors.get_memory_data(computer, hardware_type)

    assert len(snapshots) > 0


def test_get_gpu_data_when_gpu_present_returns_populated_snapshots(open_computer):
    computer, hardware_type = open_computer

    has_gpu = any(
        hardware.HardwareType in (hardware_type.GpuAmd, hardware_type.GpuNvidia)
        for hardware in computer.Hardware
    )
    if not has_gpu:
        pytest.skip("no AMD or NVIDIA GPU visible to LibreHardwareMonitor")

    snapshots = collectors.get_gpu_data(computer, hardware_type)

    assert len(snapshots) > 0