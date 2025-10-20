import psutil
import GPUtil
import cpuinfo
import pprint
import pandas as pd


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
        
        Processlist.sort(key=sortmem, reverse=True)[]

        print(Processlist)


    def get_telemetry(self):

        data = {
                #"CPU": [cpuinfo.get_cpu_info()['brand_raw']],
                "Cores": [psutil.cpu_count(logical=False)],
                "Logical Processors": [psutil.cpu_count()],
                "CPU Utilization": [f"{psutil.cpu_percent()}%"],
                "CPU Frequency": [psutil.cpu_freq().current],
                "Total Memory in GB": [round(psutil.virtual_memory()[0]/1024**3,1)],
                "Memory Utilization in GB": [round(psutil.virtual_memory()[3]/1024**3,1)],
                "Memory Utilization": [f"{psutil.virtual_memory()[2]}%"],
                "Disk Utilization":  [psutil.disk_io_counters()],
        }

        df =pd.DataFrame(data)
        df=df.to_string()
        return df

system = Sysdata()
print(system.get_top_processes())
