import GPUtil
def get_gpu_info():
        try:
            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                return {
                    "name": gpu.name,
                    "total memory": float(round(gpu.memoryTotal /1024)),
                    "used memory": round(gpu.memoryUsed /1024,1),
                    "utilization": round(gpu.load),
                    "memory utilization": round(gpu.memoryUtil*100),
                    "temperature": round(gpu.temperature)
                }
        except:
            pass
