import psutil
import cpuinfo
import GPUtil
import pandas as pd
import os


class Sysdata:
    def get_top_processes(self):


        Processlist = []
        for p in psutil.process_iter(['name']):
            process= psutil.Process(pid=p.pid)
            Processlist.append(process.as_dict(attrs= ['name','cpu_percent','memory_percent'] ))
        
        for d in Processlist:
            for k,v in d.items():
                if k == 'memory_percent':
                     d[k] = round(v,1)
        
        def sortmem(e):
            return e['memory_percent']
        
        Processlist.sort(key=sortmem, reverse=True)

        return Processlist[:5]
    
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


    def get_telemetry(self):
        gpu_info =  Sysdata.get_gpu_info()
        gpuname = ",".join(gpu_info.get("Names", "No GPU Detected"))


        data = {
                #"CPU": [cpuinfo.get_cpu_info()['brand_raw']],
                "Cores": [psutil.cpu_count(logical=False)],
                "Logical Processors": [psutil.cpu_count()],
                "CPU Utilization": [f"{psutil.cpu_percent()}%"],
                "CPU Frequency": [psutil.cpu_freq().current],
                "Total Memory": [f"{round(psutil.virtual_memory().total/1024**3,1)} GB"],
                "Memory Utilization": [f"{round(psutil.virtual_memory().used/1024**3,1)} GB"],
                "Memory Utilization": [f"{psutil.virtual_memory().percent}%"],
                "Disk Capacity": [f"{round(psutil.disk_usage("C:\\").total/1024**3)} GB"],
                "Disk Utilization": [f"{round(psutil.disk_usage("C:\\").used/1024**3)} GB"],
                "Disk Utilization": [f"{psutil.disk_usage("c:\\").percent}%"],
                #"Bytes sent in KB": [psutil.net_io_counters(pernic=True)['lo'][0]/1024],
                #"Bytes recived in KB": [psutil.net_io_counters(pernic=True)['lo'][1]/1024]
                "GPU": [",".join(gpu_info.get("Names", "No GPU Detected"))],
                "GPU Utilization": [f"{",".join(gpu_info.get("Utilization", "0"))}%"],
                "Total GPU Memory": [f"{",".join(gpu_info.get("TotalMemory", "0"))} GB"],
                "Used GPU Memory": [f"{",".join(gpu_info.get("UsedMemory", "0"))} GB"],
                "GPU Memory Utilization": [f"{",".join(gpu_info.get("MemUtilization", "0"))}%"],
                "GPU Temperature": [f"{",".join(gpu_info.get("Temperature", "0"))} C"]
}

        df =pd.DataFrame(data)
        df=df.to_string()
        return df

system = Sysdata()
#print(system.get_top_processes())
print(system.get_telemetry())



