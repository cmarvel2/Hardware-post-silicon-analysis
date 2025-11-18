class Sysdata:
    def get_top_processes(self):
        Processlist = []
        UniqProcesslist =[]

        for p in psutil.process_iter(['name']):
            try:
                process = psutil.Process(pid=p.pid)
                Processlist.append(process.as_dict(attrs= ['name','cpu_percent','memory_percent'] ))
            except psutil.NoSuchProcess(pid=p.pid):
                pass

        for process in Processlist:
            for k,v in process.items():
                if k == 'memory_percent' and k:
                      process[k] = round(v,1)

        for process1 in Processlist: 
                
                names_in_uniq_list = [p['name'] for p in UniqProcesslist]

                if process1['name'] not in names_in_uniq_list:
                    UniqProcesslist.append(process1)
                else:
                    for process2 in UniqProcesslist:
                        if process1['name'] == process2['name']:
                            process2['memory_percent'] += process1.get('memory_percent',0)
                            process2['cpu_percent'] += process1.get('cpu_percent',0)
                            break

        
        def sortmem(mem):
            return mem['memory_percent']
        
        UniqProcesslist.sort(key=sortmem, reverse=True)
        return UniqProcesslist[:5]