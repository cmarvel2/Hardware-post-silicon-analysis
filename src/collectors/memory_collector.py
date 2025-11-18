mem_info = psutil.virtual_memory()

"Total System Memory GB": [round(mem_info.total/1024**3,1)],
"Used System Memory GB": [round(mem_info.used/1024**3,1)],
"Memory Utilization %": [mem_info.percent],