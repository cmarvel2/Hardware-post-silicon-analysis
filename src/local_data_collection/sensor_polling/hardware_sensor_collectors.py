import logging
import pathlib 
from datetime import datetime, timezone

import clr

from local_data_collection.sensor_polling.models import HardwareDataStorage


currfile = pathlib.Path(__file__).parent.resolve()
librefile = (currfile / "libs" / "LibreHardwareMonitorLib.dll").resolve()
clr.AddReference(str(librefile))
from LibreHardwareMonitor.Hardware import Computer, HardwareType

def init_computer(cpu: bool=False, motherboard: bool=False, gpu: bool=False, memory: bool=False) -> tuple[Computer, HardwareType]:
    
    computer = Computer()
    computer.IsCpuEnabled = cpu
    computer.IsMotherboardEnabled = motherboard
    computer.IsGpuEnabled = gpu
    computer.IsMemoryEnabled = memory
    computer.Open()

    return computer, HardwareType

def get_cpu_data(computer: Computer, HardwareType: HardwareType) -> list[HardwareDataStorage]:
        sensor_list = []
        for hardware in computer.Hardware:

            if hardware.HardwareType == HardwareType.Cpu:
                hardware.Update()
                hardwarename = f"{hardware.Name} {hardware.Identifier}"

                for sensor in hardware.Sensors:
                    sensor_list.append(HardwareDataStorage(timestamp=datetime.now(timezone.utc).strftime(r"%Y%m%d_%H%M%S%f")[:-3], hardware_name=hardwarename, sensor_name=sensor.Name, sensor_type=sensor.SensorType.ToString(), sensor_value=sensor.Value))
        logging.info("CPU data ingestion completed")
        return sensor_list
    
def get_gpu_data(computer: Computer, HardwareType: HardwareType) -> list[HardwareDataStorage]:
    sensor_list = []
    for hardware in computer.Hardware:
        
        if hardware.HardwareType == HardwareType.GpuAmd or hardware.HardwareType == HardwareType.GpuNvidia:
            hardware.Update()
            hardwarename = f"{hardware.Name} {hardware.Identifier}"

            for sensor in hardware.Sensors:
                sensor_list.append(HardwareDataStorage(timestamp=datetime.now(timezone.utc).strftime(r"%Y%m%d_%H%M%S%f")[:-3], hardware_name=hardwarename, sensor_name=sensor.Name, sensor_type=sensor.SensorType.ToString(), sensor_value=sensor.Value))
    logging.info("GPU data ingestion completed")
    return sensor_list

def get_memory_data(computer: Computer, HardwareType: HardwareType) -> list[HardwareDataStorage]:
    sensor_list = []

    for hardware in computer.Hardware:

        if hardware.HardwareType == HardwareType.Memory:
            hardware.Update()
            hardwarename = f"{hardware.Name} {hardware.Identifier}"

            for sensor in hardware.Sensors:
                sensor_list.append(HardwareDataStorage(timestamp=datetime.now(timezone.utc).strftime(r"%Y%m%d_%H%M%S%f")[:-3], hardware_name=hardwarename, sensor_name=sensor.Name, sensor_type=sensor.SensorType.ToString(), sensor_value=sensor.Value))
    logging.info("Memory data ingestion completed")
    return sensor_list


