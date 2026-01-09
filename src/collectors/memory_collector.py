from pathlib import Path
import clr
import pprint

currfile = Path(__file__).parent.resolve()
librefile = (currfile / ".." / "libs" / "LibreHardwareMonitorLib.dll").resolve()
    
clr.AddReference(str(librefile))
from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType

def get_memory_metrics():

    computer = Computer()
    computer.IsMemoryEnabled = True
    computer.Open()

    wmemory_data  = {}
    wmemory_load = {}

    for hardware in computer.Hardware:

        if hardware.HardwareType == HardwareType.Memory:
            
            hardware.Update()

            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Data:
                    wmemory_data[sensor.Name] = sensor.Value   

                if sensor.SensorType == SensorType.Load:
                    wmemory_load[sensor.Name] = sensor.Value

    computer.Close()
        
    return {
        "memory_load": wmemory_load,
        "memory_data": wmemory_data,
    }
