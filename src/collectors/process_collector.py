import psutil
import pprint
def get_top_processes():
    processes = []
    new_dict = {}

    for p in psutil.process_iter():
        processes.append(p.as_dict(attrs= ['name','cpu_percent','memory_percent']))

    for name in processes:
        if name.get('name') not in new_dict:
            new_dict[name.get('name')] = name
        else:
            new_dict[name.get('name')]['cpu_percent'] += name['cpu_percent']
            new_dict[name.get('name')]['memory_percent'] += name['memory_percent']

    pprint.pp(sorted(new_dict, key=lambda mem: int(mem['memory_percent'])))


            
    '''try:
            process = psutil.Process(pid=p.pid)
            print(process)
            Processlist.append(process.as_dict(attrs= ['name','cpu_percent','memory_percent'] ))
        except psutil.NoSuchProcess(pid=p.pid):
            pass'''
        
    '''def sortmem(mem):
            return mem['memory_percent']
        
        UniqProcesslist.sort(key=sortmem, reverse=True)
        return UniqProcesslist[:5]'''
get_top_processes()