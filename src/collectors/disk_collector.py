import psutil

def get_disk_info():
    try:
        diskp = psutil.disk_partitions()
        disk_path = psutil.disk_usage(diskp[0].mountpoint)

        return {
        "Total Disk Capacity GB": [round(disk_path.total/1024**3)],
        "Used Disk Capacity GB": [round(disk_path.used/1024**3)],
        "Disk Utilization %": [disk_path.percent]
        }
    except:
        pass