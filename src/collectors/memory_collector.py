import psutil

def get_memory_info():
    mem_info = psutil.virtual_memory()
        
    return{
        "total_sys_memory": mem_info.total,
        "used_sys_memory": mem_info.used,
        "sys_memory_utilization": mem_info.percent,
    }
