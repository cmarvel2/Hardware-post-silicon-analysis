from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class HardwareDataStorage:
    timestamp: str | None
    hardware_name: str | None
    sensor_name: str | None
    sensor_type: str | None
    sensor_value: int | float | None

@dataclass(slots=True)
class HardwarePayloadSchema:
    metadata: dict[str, Any] = field(default_factory=dict)
    snapshots: list[dict[str, int | float | str | None]] = field(default_factory=list)