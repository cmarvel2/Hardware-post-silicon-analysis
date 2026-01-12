from pathlib import Path
import pprint as pp
import clr

currfile = Path(__file__).parent.resolve()
librefile = (currfile / ".." / "libs" / "LibreHardwareMonitorLib.dll").resolve()
    
clr.AddReference(str(librefile))
from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType 
 
def get_cpu_metrics():

    computer = Computer()
    computer.IsCpuEnabled = True
    computer.IsMotherboardEnabled = True
    computer.Open()

    wper_cpu_clock = {}
    wper_cpu_load = {}
    wper_cpu_temps = {}
    wper_cpu_power = {}


    for hardware in computer.Hardware:
        
        if hardware.HardwareType == HardwareType.Cpu:
            hardware.Update()
            cpuname = hardware.Name

            for sensor in hardware.Sensors:
        
                if sensor.SensorType == SensorType.Load:
                    wper_cpu_load[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Clock:
                    wper_cpu_clock[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Temperature:
                    wper_cpu_temps[sensor.Name] =sensor.Value

                elif sensor.SensorType == SensorType.Power:
                    wper_cpu_power[sensor.Name] = sensor.Value    
                    

        '''for sensor in hardware.Sensors:
            if sensor.SensorType == SensorType.Power:
                wper_cpu_power[sensor.Name] = sensor.Value'''

    computer.Close()
        
    return {cpuname :{
        "cpu_load": wper_cpu_load,
        "cpu_clock": wper_cpu_clock,
        "cpu_temperature": wper_cpu_temps,
        "cpu_power": wper_cpu_power,
    }}
        

pp.pprint(get_cpu_metrics())



    