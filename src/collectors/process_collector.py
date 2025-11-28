import psutil
import pandas as pd

def get_top_processes():
    processes = []


    for p in psutil.process_iter():
        with p.oneshot():
            processes.append({
            'name': p.name(),
            'cpu_percent': p.cpu_percent(),
            'memory_percent': p.memory_percent()

        })
    processes.sort(key=lambda mem: mem['memory_percent'], reverse=True)
    

    return processes
   
