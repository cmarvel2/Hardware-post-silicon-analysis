import psutil, GPUtil, cpuinfo, platform, subprocess
import pandas as pd


class Sysdata:
    def get_top_processes(self):

        Processlist = []
        for p in psutil.process_iter(['name']):
            process= psutil.Process(pid=p.pid)
            Processlist.append(process.as_dict(attrs= ['name','cpu_percent','memory_percent'] ))
        
        for process in Processlist:
            for k,v in process.items():
                if k == 'memory_percent' and k:
                     process[k] = round(v,1)
        
        def sortmem(mem):
            return mem['memory_percent']
        
        Processlist.sort(key=sortmem, reverse=True)

        return Processlist
    
    @classmethod
    def get_gpu_info(cls):
        gpuinfo = {
            "Names": [], 
            "TotalMemory": [], 
             "UsedMemory": [], 
            "Utilization": [], 
            "MemUtilization": [], 
            "Temperature": []
        }

        gpus = GPUtil.getGPUs()
        if not gpus:
            print("Currently Only Detects Nvidia GPUs")
        for num, gpu in enumerate(gpus):
            gpuinfo["Names"].append(gpu.name)
            gpuinfo["TotalMemory"].append(str(float(round(gpu.memoryTotal /1024))))
            gpuinfo["UsedMemory"].append(str(round(gpu.memoryUsed /1024,1)))
            gpuinfo["Utilization"].append(str(round(gpu.load)))
            gpuinfo["MemUtilization"].append(str(round(gpu.memoryUtil*100)))
            gpuinfo["Temperature"].append(str(round(gpu.temperature)))
            
        return gpuinfo
    
    @classmethod
    def system_specif_functs(self):
        Sysfunctlist = []
        CPUtemp = None
        CPUfreq = None
        
        if platform.system() == "Windows":
            command = r"""
        $MaxClockSpeed = (Get-CimInstance CIM_Processor).MaxClockSpeed
        $ProcessorPerformance = (Get-Counter -Counter "\Processor Information(_Total)\% Processor Performance").CounterSamples.CookedValue
        $CurrentClockSpeed = $MaxClockSpeed*($ProcessorPerformance/100)
        Write-Host $CurrentClockSpeed
"""
            completed = subprocess.run(["powershell", "-command", command], capture_output=True)
            Freq = float(completed.stdout) / 1000
            Sysfunctlist.append(round(Freq,2))
            
        elif platform.system() == "Linux":
            print("Ltest")
        else:
            CPUtemp = "Not Supported"
            Cpufreq = "Not Supported"

        for p in psutil.disk_partitions():
            Sysfunctlist.append(p.mountpoint)
        print(Sysfunctlist)
        return Sysfunctlist

    def get_telemetry(self):
        Sysfuncts = Sysdata.system_specif_functs()
        gpu_info =  Sysdata.get_gpu_info()
        mem_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage(Sysfuncts[2])
        cpu_temp = None
        


        data = {
                "CPU": [cpuinfo.get_cpu_info()['brand_raw']],
                "Cores": [psutil.cpu_count(logical=False)],
                "Logical Processors": [psutil.cpu_count()],
                "CPU Utilization": [f"{psutil.cpu_percent()}%"],
                "CPU Frequency": [psutil.cpu_freq().current],
                "CPU Temperature":[f"{[cpu_temp]} C"],
                "Total System Memory": [f"{round(mem_info.total/1024**3,1)} GB"],
                "Used System Memory": [f"{round(mem_info.used/1024**3,1)} GB"],
                "Memory Utilization": [f"{mem_info.percent}%"],
                "Total Disk Capacity": [f"{round(disk_info.total/1024**3)} GB"],
                "Used Disk Capacity": [f"{round(disk_info.used/1024**3)} GB"],
                "Disk Utilization": [f"{disk_info.percent}%"],
                #"Bytes sent in KB": [psutil.net_io_counters(pernic=True)['lo'][0]/1024],
                #"Bytes recived in KB": [psutil.net_io_counters(pernic=True)['lo'][1]/1024]
                "GPU": [",".join(gpu_info.get("Names", "No GPU Detected"))],
                "GPU Utilization": [f"{",".join(gpu_info.get("Utilization", "0"))}%"],
                "Total GPU Memory": [f"{",".join(gpu_info.get("TotalMemory", "0"))} GB"],
                "Used GPU Memory": [f"{",".join(gpu_info.get("UsedMemory", "0"))} GB"],
                "GPU Memory Utilization": [f"{",".join(gpu_info.get("MemUtilization", "0"))}%"],
                "GPU Temperature": [f"{",".join(gpu_info.get("Temperature", "0"))} C"]
}

        
        return data

system = Sysdata()
#pprint.pp(system.get_top_processes())
#pprint.pp(system.get_telemetry())
Sysdata.system_specif_functs()



