from collectors import *
import pprint

cpu = cpu_collector.get_static_cpu_data()
cpu1 = cpu_collector.get_cpu_usage()
cpu2 = cpu_collector.get_cpu_temps()
gpu = gpu_collector.get_gpu_info()
disk = disk_collector.get_disk_info()
memory = memory_collector.get_memory_info()
processs = process_collector.get_top_processes()

pprint.pp(cpu)
pprint.pp(cpu1)
pprint.pp(cpu2)
pprint.pp(gpu)
pprint.pp(disk)
pprint.pp(memory)