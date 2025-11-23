import platform
import wmi
import psutil
import cpuinfo
import WinTmp

def get_static_cpu_data():
    try: 
        return {
            "cpu_brand": cpuinfo.get_cpu_info()['brand_raw'],
            "cores": psutil.cpu_count(logical=False),
            "logical_processors": psutil.cpu_count()
        }
    except:
        pass 

def get_cpu_usage():
    try:
        if platform.system() == "Windows":
            freq = wmi.WMI(namespace="root\\cimv2")

            processor_info = freq.Win32_Processor()[0]
            max_speed_mhz = int(processor_info.MaxClockSpeed)
                    
            freq_data = freq.Win32_PerfFormattedData_Counters_ProcessorInformation(Name="_Total")[0]
            freq_percent = int(freq_data.PercentProcessorPerformance)
            
            current_speed_mhz = max_speed_mhz * (freq_percent / 100.0)
            
            
            return {
                "utilization": psutil.cpu_percent(interval=0.1),
                "frequency": current_speed_mhz
            }
            
        elif platform.system() == "Linux":
            Lin_mhz = psutil.cpu_freq().current

            return{
                "utilization": psutil.cpu_percent(interval=0.1),
                "frequency": Lin_mhz
            }
    except:
        pass

def get_cpu_temps():
    try:
        if platform.system() == "Windows":
            return {"temps": round(WinTmp.CPU_Temp(), 1)}

        elif platform.system() == "Linux":
            return {"temps": psutil.sensors._temperatures()['coretemp'][0].current}
    except:
        pass


    