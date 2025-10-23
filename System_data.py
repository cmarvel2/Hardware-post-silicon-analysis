import psutil, GPUtil, cpuinfo, platform, subprocess, pprint
from pyuac import main_requires_admin


class Sysdata:
    def get_top_processes(self):

        Processlist = []
        UniqProcesslist =[]
        

        for p in psutil.process_iter(['name']):
            try:
                process = psutil.Process(pid=p.pid)
                Processlist.append(process.as_dict(attrs= ['name','cpu_percent','memory_percent'] ))
            except psutil.NoSuchProcess(pid=p.pid):
                pass

        for process in Processlist:
            for k,v in process.items():
                if k == 'memory_percent' and k:
                      process[k] = round(v,1)

        for process1 in Processlist: 
                
                names_in_uniq_list = [p['name'] for p in UniqProcesslist]

                if process1['name'] not in names_in_uniq_list:
                    UniqProcesslist.append(process1)
                else:
                    for process2 in UniqProcesslist:
                        if process1['name'] == process2['name']:
                            process2['memory_percent'] += process1.get('memory_percent',0)
                            process2['cpu_percent'] += process1.get('cpu_percent',0)
                            break
        
        #for num, processname in enumerate(UniqProcesslist)

        
        def sortmem(mem):
            return mem['memory_percent']
        
        UniqProcesslist.sort(key=sortmem, reverse=True)
        print(UniqProcesslist)
        return UniqProcesslist[:5]
    
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
    #@main_requires_admin
    def system_specif_functs(self):
        Sysfunctlist = []
        CPUtemp = None
        CPUfreq = None
        
        
        if platform.system() == "Windows":
            GHzcommand = r"""
        $MaxClockSpeed = (Get-CimInstance CIM_Processor).MaxClockSpeed
        $ProcessorPerformance = (Get-Counter -Counter "\Processor Information(_Total)\% Processor Performance").CounterSamples.CookedValue
        $CurrentClockSpeed = $MaxClockSpeed*($ProcessorPerformance/100)
        Write-Host $CurrentClockSpeed
"""
            GHzcompleted = subprocess.run(["powershell", "-command", GHzcommand], capture_output=True)
            Freq = float(GHzcompleted.stdout) / 1000
            Sysfunctlist.append(round(Freq,2))

            Cpucommand = r"""((Get-CimInstance MSAcpi_ThermalZoneTemperature -Namespace "root/wmi").CurrentTemperature / 10 - 273.15)
""" 
            Cpucompleted = subprocess.run(['powershell', "-command", Cpucommand], capture_output=True,)
            ctemp = Cpucompleted.stdout
            Sysfunctlist.append(ctemp.decode().strip())
           
            
            
            
        elif platform.system() == "Linux":
            Sysfunctlist.append(psutil.cpu_freq().current)
            Sysfunctlist.append(psutil.sensors._temperatures()['coretemp'].current())
        else:
            CPUtemp = "Not Supported"
            Cpufreq = "Not Supported"

        for p in psutil.disk_partitions():
            Sysfunctlist.append(p.mountpoint)
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
                "CPU Utilization": [f"{psutil.cpu_percent(interval=0.1)}%"],
                "CPU Frequency": [f"{Sysfuncts[0]} GHz"],
                #"CPU Temperature":[f"{[Sysfuncts[1]]} C"],
                "Total System Memory": [f"{round(mem_info.total/1024**3,1)} GB"],
                "Used System Memory": [f"{round(mem_info.used/1024**3,1)} GB"],
                "Memory Utilization": [f"{mem_info.percent}%"],
                "Total Disk Capacity": [f"{round(disk_info.total/1024**3)} GB"],
                "Used Disk Capacity": [f"{round(disk_info.used/1024**3)} GB"],
                "Disk Utilization": [f"{disk_info.percent}%"],
                "GPU": [",".join(gpu_info.get("Names", "No GPU Detected"))],
                "GPU Utilization": [f"{",".join(gpu_info.get("Utilization", "0"))}%"],
                "Total GPU Memory": [f"{",".join(gpu_info.get("TotalMemory", "0"))} GB"],
                "Used GPU Memory": [f"{",".join(gpu_info.get("UsedMemory", "0"))} GB"],
                "GPU Memory Utilization": [f"{",".join(gpu_info.get("MemUtilization", "0"))}%"],
                "GPU Temperature": [f"{",".join(gpu_info.get("Temperature", "0"))} C"]
}

        
        return data

system = Sysdata()
system.get_top_processes()
system.get_telemetry()




