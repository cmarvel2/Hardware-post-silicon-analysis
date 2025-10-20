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
        gpuinfo = []

        gpus = GPUtil.getGPUs()
        if not gpus:
            print("Nvidia GPU Detetct Only")
        for i in gpus:
            gpuinfo.append({i.name: (i.memoryTotal, i.memoryUsed, i.load, f"{round(i.memoryUtil*100)}%", i.temperature)})
        return gpuinfo


    def get_telemetry(self):

        data = {
                #"CPU": [cpuinfo.get_cpu_info()['brand_raw']],
                "Cores": [psutil.cpu_count(logical=False)],
                "Logical Processors": [psutil.cpu_count()],
                "CPU Utilization": [f"{psutil.cpu_percent()}%"],
                "CPU Frequency": [psutil.cpu_freq().current],
                "Total Memory in GB": [round(psutil.virtual_memory().total/1024**3,1)],
                "Memory Utilization in GB": [round(psutil.virtual_memory().used/1024**3,1)],
                "Memory Utilization": [f"{psutil.virtual_memory().percent}%"],
                "Disk Capacity in GB": [round(psutil.disk_usage("C:\\").total/1024**3)],
                "Disk Utilization in GB": [round(psutil.disk_usage("C:\\").used/1024**3)],
                "Disk Utilization": [f"{psutil.disk_usage("c:\\").percent}%"],
                #"Bytes sent in KB": [psutil.net_io_counters(pernic=True)['lo'][0]/1024],
                #"Bytes recived in KB": [psutil.net_io_counters(pernic=True)['lo'][1]/1024]
                "GPU": [Sysdata.get_gpu_info()],
                "GPU Utilization in GB": [Sysdata.get_gpu_info()],
                "Total GPU Memory in GB": [Sysdata.get_gpu_info()],
                "GPU Memory Utilization": [Sysdata.get_gpu_info()]
        }

        df =pd.DataFrame(data)
        df=df.to_string()
        return df

system = Sysdata()
#print(system.get_top_processes())
print(system.get_telemetry())



