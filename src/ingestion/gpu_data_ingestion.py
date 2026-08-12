import pathlib 
import clr
from pipeline_utils import logger
import logging

logger.logging_setup()
currfile = pathlib.Path(__file__).parent.resolve()
librefile = (currfile / ".." / "ingestion" / "libs" / "LibreHardwareMonitorLib.dll").resolve()
    
clr.AddReference(str(librefile))
from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType
        
gpu_computer = Computer()
gpu_computer.IsGpuEnabled = True
gpu_computer.Open()

def get_gpu_data() -> dict:
    logging.info("Starting GPU data ingestion")
    try:
        gpu_list = []

        for hardware in gpu_computer.Hardware:
            if hardware.HardwareType == HardwareType.GpuAmd:
                        
                hardware.Update()

                wgpu_clock = {}
                wgpu_load = {}
                wgpu_temperature = {}
                wgpu_power = {}

                for sensor in hardware.Sensors:
                    
                    if sensor.SensorType == SensorType.Load:
                        wgpu_load[sensor.Name] = sensor.Value

                    elif sensor.SensorType == SensorType.Clock:
                        wgpu_clock[sensor.Name] = sensor.Value

                    elif sensor.SensorType == SensorType.Temperature:
                        wgpu_temperature[sensor.Name] = sensor.Value

                    elif sensor.SensorType == SensorType.Power:
                        wgpu_power[sensor.Name] = sensor.Value

                gpu_list.append({hardware.Name: {
                "gpu_load": wgpu_load,
                "gpu_clock": wgpu_clock,
                "gpu_temperature": wgpu_temperature,
                "gpu_power": wgpu_power
                }})

            elif hardware.HardwareType == HardwareType.GpuNvidia:

                hardware.Update()

                wgpu_clock = {}
                wgpu_load = {}
                wgpu_temperature = {}
                wgpu_power = {}

                for sensor in hardware.Sensors:
                    if sensor.SensorType == SensorType.Load:
                        wgpu_load[sensor.Name] = sensor.Value

                    elif sensor.SensorType == SensorType.Clock:
                        wgpu_clock[sensor.Name] = sensor.Value

                    elif sensor.SensorType == SensorType.Temperature:
                        wgpu_temperature[sensor.Name] = sensor.Value

                    elif sensor.SensorType == SensorType.Power:
                        wgpu_power[sensor.Name] = sensor.Value

                gpu_list.append({hardware.Name: {
                "gpu_load": wgpu_load,
                "gpu_clock": wgpu_clock,
                "gpu_temperature": wgpu_temperature,
                "gpu_power": wgpu_power
                }})
        logging.info(f"GPU data ingestion completed")
        return {"gpus": gpu_list}
    except Exception as e:
        logging.error(f"Error {e} ingesting data from GPU sensors")
        raise
