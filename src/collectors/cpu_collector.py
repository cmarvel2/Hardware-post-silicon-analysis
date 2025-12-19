import platform
import psutil
import cpuinfo 
from pathlib import Path
import pprint
import clr

if platform.system() == "Windows":
    currfile = Path(__file__).parent.resolve()
    librefile = (currfile / ".." / "libs" / "LibreHardwareMonitorLib.dll").resolve()
        
    clr.AddReference(str(librefile))
    from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType, IVisitor

def get_static_cpu_data():
 
    return {
        "cpu_brand": cpuinfo.get_cpu_info()['brand_raw'],
        "p_cores": psutil.cpu_count(logical=False),
        "l_cores": psutil.cpu_count()
    }
 

def get_cpu_usage():
    
    if platform.system() == "Windows":

        computer = Computer()
        computer.IsCpuEnabled = True
        computer.IsMotherboardEnabled = True
        computer.Open()

        wper_cpu_freq = {}
        wper_cpu_percent = {}
        wper_cpu_temps = {}
        wper_cpu_volts = {}
        wper_cpu_watts = {}


        for hardware in computer.Hardware:
            if hardware.HardwareType == HardwareType.Cpu:
                     
                hardware.Update()

                for sensor in hardware.Sensors:
                    if sensor.SensorType == SensorType.Load:
                        wper_cpu_percent[sensor.Name] =sensor.Value

                    elif sensor.SensorType == SensorType.Clock:
                        wper_cpu_freq[sensor.Name] =sensor.Value

                    elif sensor.SensorType == SensorType.Temperature:
                        wper_cpu_temps[sensor.Name] =sensor.Value

                    elif sensor.SensorType == SensorType.Voltage:
                        wper_cpu_volts[sensor.Name] = sensor.Value

            for sensor in hardware.Sensors:
                if sensor.SensorType == SensorType.Power:
                    wper_cpu_watts[sensor.Name] = sensor.Value

        computer.Close()
            
        return {
            "utilization_per_cpu": wper_cpu_percent,
            "frequency_per_cpu": wper_cpu_freq,
            "temperature_per_cpu": wper_cpu_temps,
            "voltage_per_cpu": wper_cpu_volts,
            "power_per_cpu": wper_cpu_watts
        }
            
pprint.pprint(get_cpu_usage())




    