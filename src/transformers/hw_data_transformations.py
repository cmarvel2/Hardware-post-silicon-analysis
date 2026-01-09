from collectors import *
import pprint as pp
import winreg

def cpu_dict_transformer(cpudata, time):
    cpulst = []
    
    for hwname, field in cpudata.items():
        for hwfield, hwsubpartdict in field.items():
            for hwsubpart, value in hwsubpartdict.items():
                if "Core" in hwsubpart:
                    cpulst.append({'hardware_name': hwname,
                        'hardware_field': hwfield,
                        'sensor_name': hwsubpart,
                        'sensor_value': value,
                        'timestamp': time
                        })
                elif "Package" in hwsubpart:
                    cpulst.append({'hardware_name': hwname,
                        'hardware_field': hwfield,
                        'sensor_name': hwsubpart,
                        'sensor_value': value,
                        'timestamp': time
                        })
                elif "Total" in hwsubpart:
                    cpulst.append({'hardware_name': hwname,
                        'hardware_field': hwfield,
                        'sensor_name': hwsubpart,
                        'sensor_value': value,
                        'timestamp': time
                        })
    
    return cpulst
            

def gpu_dict_transformer(gpudata, time):
    gpulst = []

    for gpu in gpudata:
        for hwname, field in gpu.items():
            for hwfield, hwsubpartdict in field.items():
                for hwsubpart, value in hwsubpartdict.items():
                    if "Core" in hwsubpart and hwfield != 'gpu_power':
                        gpulst.append({'hardware_name': hwname,
                        'hardware_field': hwfield,
                        'sensor_name': hwsubpart,
                        'sensor_value': value,
                        'timestamp': time
                        })
                    elif 'Memory' in hwsubpart:
                        gpulst.append({'hardware_name': hwname,
                        'hardware_field': hwfield,
                        'sensor_name': hwsubpart,
                        'sensor_value': value,
                        'timestamp': time
                        })
                    elif 'Package' in hwsubpart:
                        gpulst.append({'hardware_name': hwname,
                        'hardware_field': hwfield,
                        'sensor_name': hwsubpart,
                        'sensor_value': value,
                        'timestamp': time
                        })
                    elif "Hot Spot" in hwsubpart:
                        gpulst.append({'hardware_name': hwname,
                        'hardware_field': hwfield,
                        'sensor_name': hwsubpart,
                        'sensor_value': value,
                        'timestamp': time
                        })

    return gpulst
                    
                    

def memory_dict_transformer(memorydata, time):
    memorylst = []

    for hwfieldname, field in memorydata.items():
        for sensorname, value in field.items():
            memorylst.append({
                        'hardware_name': 'RAM',
                        'hardware_field': hwfieldname,
                        'sensor_name': sensorname,
                        'sensor_value': value,
                        'timestamp': time
                        })
            
    return memorylst

def get_machine_uuid():
    key_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Cryptography', 0, access=winreg.KEY_READ)
    uuid = winreg.QueryValueEx(key_handle, 'MachineGuid')
    winreg.CloseKey(key_handle)

    realuuid, _ = uuid

    if realuuid == str and len(realuuid) == 36:
        return realuuid