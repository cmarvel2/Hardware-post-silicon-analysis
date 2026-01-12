import clr
from pathlib import Path
import pprint

currfile = Path(__file__).parent.resolve()
librefile = (currfile / ".." / "libs" / "LibreHardwareMonitorLib.dll").resolve()
    
clr.AddReference(str(librefile))
from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType
        
def get_gpu_metrics():

    computer = Computer()
    computer.IsGpuEnabled = True
    computer.Open()

    gpus = []

    wgpu_clock = {}
    wgpu_load = {}
    wgpu_temperature = {}
    wgpu_power = {}
    wgpu_fan = {}

    for hardware in computer.Hardware:
        if hardware.HardwareType == HardwareType.GpuAmd:
                    
            hardware.Update()

            for sensor in hardware.Sensors:
                
                if sensor.SensorType == SensorType.Load:
                    wgpu_load[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Clock:
                    wgpu_clock[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Temperature:
                    wgpu_temperature[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Power:
                    wgpu_power[sensor.Name] = sensor.Value


            gpus.append({hardware.Name: {
            "gpu_load": wgpu_load,
            "gpu_clock": wgpu_clock,
            "gpu_temperature": wgpu_temperature,
            "gpu_fan": wgpu_fan,
            "gpu_power": wgpu_power
            }})

        elif hardware.HardwareType == HardwareType.GpuNvidia:

            hardware.Update()

            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Load:
                    wgpu_load[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Clock:
                    wgpu_clock[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Temperature:
                    wgpu_temperature[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Power:
                    wgpu_power[sensor.Name] = sensor.Value

            gpus.append({hardware.Name: {
            "gpu_load": wgpu_load,
            "gpu_clock": wgpu_clock,
            "gpu_temperature": wgpu_temperature,
            "gpu_power": wgpu_power
            }})

    computer.Close()

    return gpus
                