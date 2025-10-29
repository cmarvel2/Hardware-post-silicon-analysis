import psutil, GPUtil, cpuinfo, platform, WinTmp, wmi

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

        
        def sortmem(mem):
            return mem['memory_percent']
        
        UniqProcesslist.sort(key=sortmem, reverse=True)
        return UniqProcesslist[:5]
    
    def get_gpu_info(self):
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
    
    def system_specif_functs(self):
        Sysfunctlist = []
    
        if platform.system() == "Windows":
            freq = wmi.WMI(namespace="root\\cimv2")

            processor_info = freq.Win32_Processor()[0]
            max_speed_mhz = int(processor_info.MaxClockSpeed)
                    
            freq_data = freq.Win32_PerfFormattedData_Counters_ProcessorInformation(Name="_Total")[0]
            freq_percent = int(freq_data.PercentProcessorPerformance)
            
            current_speed_mhz = max_speed_mhz * (freq_percent / 100.0)
            freq_ghz = round(current_speed_mhz / 1000, 2)
            
            Sysfunctlist.append(freq_ghz)

            Sysfunctlist.append(round(WinTmp.CPU_Temp(), 1))
            
        elif platform.system() == "Linux":
            Sysfunctlist.append(psutil.cpu_freq().current)
            Sysfunctlist.append(psutil.sensors._temperatures()['coretemp'].current())
        else:
            Sysfunctlist.append("Not Supported")
            Sysfunctlist.append("Not Supported")

        for p in psutil.disk_partitions():
            Sysfunctlist.append(p.mountpoint)
        
        return Sysfunctlist

    def get_telemetry(self):
        Sysfuncts = self.system_specif_functs()
        gpu_info =  self.get_gpu_info()
        mem_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage(Sysfuncts[2])
        


        data = {
                "CPU": [cpuinfo.get_cpu_info()['brand_raw']],
                "Cores": [psutil.cpu_count(logical=False)],
                "Logical Processors": [psutil.cpu_count()],
                "CPU Utilization %": [psutil.cpu_percent(interval=0.1)],
                "CPU Frequency GHz": [Sysfuncts[0]],
                "CPU Temperature C": [Sysfuncts[1]],
                "Total System Memory GB": [round(mem_info.total/1024**3,1)],
                "Used System Memory GB": [round(mem_info.used/1024**3,1)],
                "Memory Utilization %": [mem_info.percent],
                "Total Disk Capacity GB": [round(disk_info.total/1024**3)],
                "Used Disk Capacity GB": [round(disk_info.used/1024**3)],
                "Disk Utilization %": [disk_info.percent],
                "GPU": [",".join(gpu_info.get("Names", "No GPU Detected"))],
                "GPU Utilization %": [float(",".join(gpu_info.get("Utilization", '0')))],
                "Total GPU Memory GB": [float(",".join(gpu_info.get("TotalMemory", '0')))],
                "Used GPU Memory GB": [float(",".join(gpu_info.get("UsedMemory", '0')))],
                "GPU Memory Utilization %": [float(",".join(gpu_info.get("MemUtilization", '0')))],
                "GPU Temperature C": [float(",".join(gpu_info.get("Temperature", '0')))]
}
        return data





