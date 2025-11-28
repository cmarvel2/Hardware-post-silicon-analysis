from collectors import *
from transformers import telemetry_transformer


def collect_all_data():
    cpu = cpu_collector.get_static_cpu_data()
    cpu1 = cpu_collector.get_cpu_usage()
    cpu2 = cpu_collector.get_cpu_temps()
    gpu = gpu_collector.get_gpu_info()
    disk = disk_collector.get_disk_info()
    memory = memory_collector.get_memory_info()
    processs = process_collector.get_top_processes()

    
def transform_all_data():
    tcpu = telemetry_transformer.cpu_agg_transformer(cpu,cpu1,cpu2)
    tgpu = telemetry_transformer.gpu_transformer(gpu)
    tmem = telemetry_transformer.memory_transformer(memory)
    tdisk = telemetry_transformer.disk_transformer(disk)

    hw = telemetry_transformer.hardware_aggregate(tcpu, tgpu, tmem, tdisk)

    print(hw)