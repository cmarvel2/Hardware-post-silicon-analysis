from collectors import *
from transformers import telemetry_transformer


def run_pipeline():
    cpu = cpu_collector.get_static_cpu_data()
    cpu1 = cpu_collector.get_cpu_usage()
    cpu2 = cpu_collector.get_cpu_temps()
    gpu = gpu_collector.get_gpu_info()
    disk = disk_collector.get_disk_info()
    memory = memory_collector.get_memory_info()
    processs = process_collector.get_top_processes()

    tcpu = telemetry_transformer.cpu_agg_transformer(cpu,cpu1,cpu2)
    tmem = telemetry_transformer.memory_transformer(memory)
    tprocess = telemetry_transformer.process_transformer(processs)

    tgpu = telemetry_transformer.gpu_transformer(gpu)
    tdisk = telemetry_transformer.disk_transformer(disk)
    hwagg = telemetry_transformer.cpu_mem_aggregate(tcpu, tmem,)
    
    

run_pipeline()

