from pathlib import Path
import clr

currfile = Path(__file__).parent.resolve()
librefile = (currfile / ".." / "libs" / "LibreHardwareMonitorLib.dll").resolve()
    
clr.AddReference(str(librefile))
from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType 
 
cpu_computer = Computer()
cpu_computer.IsCpuEnabled = True
cpu_computer.IsMotherboardEnabled = True
cpu_computer.Open()

def get_cpu_metrics():

    wper_cpu_clock = {}
    wper_cpu_load = {}
    wper_cpu_temps = {}
    wper_cpu_power = {}

    for hardware in cpu_computer.Hardware:
        
        if hardware.HardwareType == HardwareType.Cpu:
            hardware.Update()
            cpuname = hardware.Name

            for sensor in hardware.Sensors:
        
                if sensor.SensorType == SensorType.Load:
                    wper_cpu_load[sensor.Name] = sensor.Value

                elif sensor.SensorType == SensorType.Clock:
                    wper_cpu_clock[sensor.Name] = sensor.Value

                elif sensor.SensorType == SensorType.Temperature:
                    wper_cpu_temps[sensor.Name] = sensor.Value

                elif sensor.SensorType == SensorType.Power:
                    wper_cpu_power[sensor.Name] = sensor.Value

    return {cpuname: {
        "cpu_load": wper_cpu_load,
        "cpu_clock": wper_cpu_clock,
        "cpu_temperature": wper_cpu_temps,
        "cpu_power": wper_cpu_power,
    }}