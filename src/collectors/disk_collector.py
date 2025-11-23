import psutil

def get_disk_info():
    disk_list = []
    try:
        for index, partition in enumerate(psutil.disk_partitions(all=False)):
            disk_path = psutil.disk_usage(partition.mountpoint)
            print({"disk": index,
            "total_disk_capacity": disk_path.total,
            "used_disk_capacity": disk_path.used,
            "disk_utilization": disk_path.percent
        })
            disk_list.append({
            "disk": index,
            "total _disk Capacity": disk_path.total,
            "used_disk Capacity": disk_path.used,
            "disk_utilization": disk_path.percent
        })
            
        return disk_list
    except:
        pass

get_disk_info()