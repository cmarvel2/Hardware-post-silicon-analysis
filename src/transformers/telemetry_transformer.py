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
    gpulst=[]
    for row in rawgpu:
        gpulst.append({
            'gpu': row['gpu'],
            'gpu_name': row['gpu_name'],
            'total_gpu_memory': round(row['total_gpu_memory'] /1024.0),
            'used_gpu_memory': round(row['used_gpu_memory'] /1024.0),
            'gpu_utilization': round(row['gpu_utilization']),
            'gpu_memory_utilization': round(row['gpu_memory_utilization']*100),
            'gpu_temp': row['gpu_temp']

        })

    return gpulst

def memory_transformer(rawmem):
    return {
        'total_sys_memory': round(rawmem['total_sys_memory']/1024**3),
        'used_sys_memory': round(rawmem['used_sys_memory']/1024**3),
        'memory_utilization': rawmem['sys_memory_utilization']
    }

def disk_transformer(rawdisk):
    disklst = []
    for row in rawdisk: 
        disklst.append({
            'disk': row['disk'],
            'total_disk_capacity': row['total_disk_capacity'],
            'used_disk_capacity': row['used_disk_capacity']    
        })
    
    return disklst

def process_transformer():
    pass

def hardware_aggregate(tcpu,tgpu,tmem,tdisk):


    hwagg = [tcpu, tmem]
    hwagg.extend(tdisk)
    hwagg.extend(tgpu)

    return hwagg
