import psutil


def get_top_processes():
    processes = []
    for process in psutil.process_iter():
        processes.append(process.as_dict(attrs= ['pid', 'name','cpu_percent','memory_percent'] ))

    return processes
    

