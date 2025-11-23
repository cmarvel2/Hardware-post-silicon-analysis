import psutil

def get_memory_info():
    try:
        mem_info = psutil.virtual_memory()
        return{
        "Total System Memory": mem_info.total,
        "Used System Memory": mem_info.used,
        "Memory Utilization": mem_info.percent,
        }
    except:
        pass