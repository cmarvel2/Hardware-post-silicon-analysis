import re

import pytest

pytest.importorskip("clr")

from local_data_collection.sensor_polling import hardware_sensor_collectors as collectors  
from local_data_collection.sensor_polling.models import HardwareDataStorage  


class FakeSensorType:
    def __init__(self, label):
        self._label = label

    def ToString(self):
        return self._label


class FakeSensor:
    def __init__(self, name="CPU Core #1", sensor_type="Temperature", value=42.5):
        self.Name = name
        self.SensorType = FakeSensorType(sensor_type)
        self.Value = value


class FakeHardware:
    def __init__(self, name, identifier, hardware_type, sensors):
        self.Name = name
        self.Identifier = identifier
        self.HardwareType = hardware_type
        self.Sensors = sensors
        self.update_call_count = 0

    def Update(self):
        self.update_call_count += 1


class FakeComputer:
    def __init__(self, hardware):
        self.Hardware = hardware


@pytest.fixture
def hardware_type():
    return collectors.HardwareType


def make_cpu_hardware(sensors=None):
    return FakeHardware(
        name="Intel i7",
        identifier="/intelcpu/0",
        hardware_type=collectors.HardwareType.Cpu,
        sensors=sensors if sensors is not None else [FakeSensor()],
    )


class TestGetCpuData:

    def test_when_hardware_is_cpu_returns_one_snapshot_per_sensor(self, hardware_type):
        cpu = make_cpu_hardware(sensors=[FakeSensor(name="Core #1"), FakeSensor(name="Core #2")])
        computer = FakeComputer([cpu])

        snapshots = collectors.get_cpu_data(computer, hardware_type)

        assert len(snapshots) == 2

    def test_when_hardware_is_not_cpu_returns_empty_list(self, hardware_type):
        memory = FakeHardware(
            name="Generic Memory",
            identifier="/ram/0",
            hardware_type=hardware_type.Memory,
            sensors=[FakeSensor()],
        )
        computer = FakeComputer([memory])

        assert collectors.get_cpu_data(computer, hardware_type) == []

    def test_when_hardware_is_cpu_calls_update_before_reading(self, hardware_type):
        cpu = make_cpu_hardware()
        computer = FakeComputer([cpu])

        collectors.get_cpu_data(computer, hardware_type)

        assert cpu.update_call_count == 1

    def test_when_hardware_is_not_cpu_does_not_call_update(self, hardware_type):
        memory = FakeHardware(
            name="Generic Memory",
            identifier="/ram/0",
            hardware_type=hardware_type.Memory,
            sensors=[FakeSensor()],
        )
        computer = FakeComputer([memory])

        collectors.get_cpu_data(computer, hardware_type)

        assert memory.update_call_count == 0

    def test_when_cpu_has_no_sensors_returns_empty_list(self, hardware_type):
        computer = FakeComputer([make_cpu_hardware(sensors=[])])

        assert collectors.get_cpu_data(computer, hardware_type) == []

    def test_when_snapshot_is_built_maps_sensor_fields(self, hardware_type):
        computer = FakeComputer(
            [make_cpu_hardware(sensors=[FakeSensor(name="Core #1", sensor_type="Clock", value=3600.0)])]
        )

        snapshot = collectors.get_cpu_data(computer, hardware_type)[0]

        assert snapshot.sensor_name == "Core #1"
        assert snapshot.sensor_type == "Clock"
        assert snapshot.sensor_value == 3600.0

    def test_when_snapshot_is_built_sets_hardware_name_to_name_and_identifier(self, hardware_type):
        computer = FakeComputer([make_cpu_hardware()])

        snapshot = collectors.get_cpu_data(computer, hardware_type)[0]

        assert snapshot.hardware_name == "Intel i7 /intelcpu/0"

    def test_when_snapshot_is_built_formats_timestamp_as_utc_datetime_with_milliseconds(self, hardware_type):
        computer = FakeComputer([make_cpu_hardware()])

        snapshot = collectors.get_cpu_data(computer, hardware_type)[0]

        assert re.fullmatch(r"\d{8}_\d{9}", snapshot.timestamp)

    def test_when_sensor_value_is_none_stores_none(self, hardware_type):
        computer = FakeComputer([make_cpu_hardware(sensors=[FakeSensor(value=None)])])

        snapshot = collectors.get_cpu_data(computer, hardware_type)[0]

        assert snapshot.sensor_value is None

    def test_when_snapshots_are_built_returns_hardware_data_storage_instances(self, hardware_type):
        computer = FakeComputer([make_cpu_hardware()])

        snapshots = collectors.get_cpu_data(computer, hardware_type)

        assert all(isinstance(snapshot, HardwareDataStorage) for snapshot in snapshots)


class TestGetGpuData:

    @pytest.mark.parametrize(
        "gpu_enum_member",
        ["GpuAmd", "GpuNvidia"],
        ids=["gpu_amd", "gpu_nvidia"],
    )
    def test_when_hardware_is_gpu_returns_snapshots(self, hardware_type, gpu_enum_member):
        gpu = FakeHardware(
            name="Radeon RX",
            identifier="/gpu/0",
            hardware_type=getattr(hardware_type, gpu_enum_member),
            sensors=[FakeSensor(name="GPU Hot Spot")],
        )
        computer = FakeComputer([gpu])

        snapshots = collectors.get_gpu_data(computer, hardware_type)

        assert len(snapshots) == 1
        assert snapshots[0].sensor_name == "GPU Hot Spot"

    def test_when_hardware_is_not_gpu_returns_empty_list(self, hardware_type):
        cpu = make_cpu_hardware()
        computer = FakeComputer([cpu])

        assert collectors.get_gpu_data(computer, hardware_type) == []


class TestGetMemoryData:

    def test_when_hardware_is_memory_returns_snapshots(self, hardware_type):
        memory = FakeHardware(
            name="Generic Memory",
            identifier="/ram/0",
            hardware_type=hardware_type.Memory,
            sensors=[FakeSensor(name="Memory Used")],
        )
        computer = FakeComputer([memory])

        snapshots = collectors.get_memory_data(computer, hardware_type)

        assert len(snapshots) == 1
        assert snapshots[0].sensor_name == "Memory Used"

    def test_when_hardware_is_not_memory_returns_empty_list(self, hardware_type):
        computer = FakeComputer([make_cpu_hardware()])

        assert collectors.get_memory_data(computer, hardware_type) == []