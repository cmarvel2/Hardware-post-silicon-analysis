import psutil

def get_memory_info():
    try:
        mem_info = psutil.virtual_memory()
        return{
        "Total System Memory GB": [round(mem_info.total/1024**3,1)],
        "Used System Memory GB": [round(mem_info.used/1024**3,1)],
        "Memory Utilization %": [mem_info.percent],
        }
    except:
        pass