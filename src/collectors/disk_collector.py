import psutil


def get_disk_info():
    disk_list = []
    
    for partition in psutil.disk_partitions(all=False):
        disk_path = psutil.disk_usage(partition.mountpoint)
            
        disk_list.append({
            "total_disk_capacity": disk_path.total,
            "used_disk_capacity": disk_path.used,
           
    })
            
    return disk_list
