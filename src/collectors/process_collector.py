import psutil
import pprint
def get_top_processes():
    processes = []

    for p in psutil.process_iter():
        processes.append(p.as_dict(attrs= ['pid','name','cpu_percent','memory_percent']))

    return processes
