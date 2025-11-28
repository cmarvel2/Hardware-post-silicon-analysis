import GPUtil
def get_gpu_info():
        try:
            gpu_list = []
            gpus = GPUtil.getGPUs()
            for index, gpu in enumerate(gpus):
                gpu_list.append({
                    "gpu": index,
                    "gpu_name": gpu.name,
                    "total_gpu_memory": gpu.memoryTotal,
                    "used_gpu_memory": gpu.memoryUsed,
                    "gpu_utilization": gpu.load,
                    "gpu_memory_utilization": gpu.memoryUtil,
                    "gpu_temp": gpu.temperature
                })

            return gpu_list
        except:
            pass
