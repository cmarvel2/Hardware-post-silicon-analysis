import pandas as pd

def cpu_agg_transformer(rawcpu, rawcpu1, rawcpu2):
    return {
        "cpu_brand": rawcpu['cpu_brand'],
        "p_cores": rawcpu['p_cores'],
        'l_cores': rawcpu['l_cores'],
        'cpu_utilization': rawcpu1['cpu_utilization'],
        'cpu_frequency': round(rawcpu1['cpu_frequency'] / 1000, 2),
        'cpu_temp': rawcpu2['cpu_temp']
        
    }

def gpu_transformer(rawgpu):
    gpus={}
    for index, gpu in enumerate(rawgpu):
        g = f"gpu_{index}"
        gpus.update({
            f"{g}_name": gpu['name'],
            f"total_{g}_memory": round(gpu["total_gpu_memory"]/1024**3, 1),
            f"used_{g}_memory": round(gpu["used_gpu_memory"]/1024**3, 1),
            f"{g}_utilization": gpu["gpu_utilization"],
            f"{g}_memory_utilization": round(gpu["gpu_memory_utilization"]*100,1),
            f"{g}_temp": gpu["gpu_temp"]
            
        })
        

    return gpus

def memory_transformer(rawmem):
    return {
        'total_sys_memory': round(rawmem['total_sys_memory']/1024**3, 1),
        'used_sys_memory': round(rawmem['used_sys_memory']/1024**3, 1),
        'memory_utilization': rawmem['sys_memory_utilization']
    }

def disk_transformer(rawdisk):
    disks = {}
    for index, disk in enumerate(rawdisk):
        d = f"disk_{index}"
        disks.update({
            f"total_{d}_capacity": round(disk["total_disk_capacity"]/1024**3),
            f"used{d}_capacity": round(disk["used_disk_capacity"]/1024**3)

        })

    return disks

def process_transformer():
    pass

def hardware_aggregate(tcpu,tgpu,tmem,tdisk):


    hwagg = {}
    hwagg.update(tcpu)
    hwagg.update(tmem)
    hwagg.update(tdisk)
    hwagg.update(tgpu)

    #df = pd.DataFrame([hwagg])

    return hwagg
