from collectors import *
from transformers import telemetry_transformer
from utils.logger  import setup_logs, function_logs

log = setup_logs()


def run_pipeline():
    log.info("Pipeline Running")

    
    
    cpu = function_logs(cpu_collector.get_static_cpu_data,log)

    
    cpu1 = function_logs(cpu_collector.get_cpu_usage,log)

    
    cpu2 = function_logs(cpu_collector.get_cpu_temps,log)

    
    gpu = function_logs(gpu_collector.get_gpu_info,log)

    
    disk = function_logs(disk_collector.get_disk_info,log)

   
    memory = function_logs(memory_collector.get_memory_info,log)

    
    processs = function_logs(process_collector.get_top_processes,log)

    
    tcpu = function_logs(telemetry_transformer.cpu_agg_transformer,log,cpu,cpu1,cpu2)

    
    tmem = function_logs(telemetry_transformer.memory_transformer,log,memory)

    
    tprocess = function_logs(telemetry_transformer.process_transformer,log,processs)

    
    tgpu = function_logs(telemetry_transformer.gpu_transformer,log,gpu)

    
    tdisk = function_logs(telemetry_transformer.disk_transformer,log,disk)

    
    hwagg = function_logs(telemetry_transformer.cpu_mem_aggregate,log,tcpu, tmem,)

