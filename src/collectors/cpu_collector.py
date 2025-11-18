import platform
import wmi
import psutil
import cpuinfo
import WinTmp

def get_static_cpu_data():
    try: 
        return {
            "cpu name": cpuinfo.get_cpu_info()['brand_raw'],
            "cores": psutil.cpu_count(logical=False),
            "logical processors": psutil.cpu_count()
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
            freq_ghz = round(current_speed_mhz / 1000, 2)
            
            return {
                "utilization": psutil.cpu_percent(interval=0.1),
                "frequency": freq_ghz
            }
            
        elif platform.system() == "Linux":

            return{
                "utilization": psutil.cpu_percent(interval=0.1),
                "frequency": psutil.cpu_freq().current
            }
    except:
        pass

def get_cpu_temps():
    try:
        if platform.system() == "Windows":
            return {"temps": round(WinTmp.CPU_Temp(), 1)}

        elif platform.system == "Linux":
            return {"temps": psutil.sensors._temperatures()['coretemp'][0].current}
    except:
        pass

def cpu_data_assembly():
    static = get_static_cpu_data()
    usage = get_cpu_usage()
    temps = get_cpu_temps()

    print({"cpu name": static.get("cpu name"),
        "cores": static.get("cores"),
        "logical processors": static.get("logical processors"),
        "utilization": usage.get("utilization"),
        "frequency": usage.get("frequency"),
        "temps": temps.get("temps")})

    return {
        "cpu name": static.get("cpu name"),
        "cores": static.get("cores"),
        "logical processors": static.get("logical processors"),
        "utilization": usage.get("utilization"),
        "freqeuncy": usage.get("frequency"),
        "temps": temps.get("temps")
    }



    