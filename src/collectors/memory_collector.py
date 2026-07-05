from pathlib import Path
import clr

currfile = Path(__file__).parent.resolve()
librefile = (currfile / ".." / "libs" / "LibreHardwareMonitorLib.dll").resolve()
    
clr.AddReference(str(librefile))
from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType

memory_computer = Computer()
memory_computer.IsMemoryEnabled = True
memory_computer.Open()

def get_memory_metrics():

    wmemory_data = {}
    wmemory_load = {}

    for hardware in memory_computer.Hardware:

        if hardware.HardwareType == HardwareType.Memory:
            
            hardware.Update()

            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Data:
                    wmemory_data[sensor.Name] = sensor.Value   

                if sensor.SensorType == SensorType.Load:
                    wmemory_load[sensor.Name] = sensor.Value
        
    return {
        "memory_load": wmemory_load,
        "memory_data": wmemory_data,
    }
