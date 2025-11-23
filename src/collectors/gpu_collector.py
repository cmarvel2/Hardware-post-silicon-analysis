import GPUtil
def get_gpu_info():
        try:
            gpu_list = []
            gpus = GPUtil.getGPUs()
            for index, gpu in enumerate(gpus):
                gpu_list.append({
                    "GPU": index,
                    "name": gpu.name,
                    "total_memory": gpu.memoryTotal,
                    "used_memory": gpu.memoryUsed,
                    "utilization": gpu.load,
                    "memory_utilization": gpu.memoryUtil,
                    "temperature": gpu.temperature
                })

            return gpu_list
        except:
            pass
