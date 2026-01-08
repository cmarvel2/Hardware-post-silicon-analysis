from collectors import *
import pprint as pp

def cpu_dict_transformer(cpudata):
    
    for hwname, field in cpudata.items():
        for hwfield, hwsubpartdict in field.items():
            for hwsubpart, value in hwsubpartdict.items():
                if "Core" in hwsubpart:
                    pp.pprint((hwsubpart, value))
                elif "Package" in hwsubpart:
                    pp.pprint((hwsubpart, value))
                elif "Total" in hwsubpart:
                    pp.pprint((hwsubpart, value))
            

def gpu_dict_transformer(gpudata):

    for gpu in gpudata:
        for hwname, field in gpu.items():
            for hwfield, hwsubpartdict in field.items():
                for hwsubpart, value in hwsubpartdict.items():
                    if "Core" in hwsubpart and hwfield != 'gpu_power':
                        pp.pprint((hwsubpart, value))
                    elif 'Memory' in hwsubpart:
                        pp.pprint((hwsubpart, hwfield, value))
                    elif 'Package' in hwsubpart:
                        pp.pprint((hwsubpart, hwfield, value))
                    elif "Hot Spot" in hwsubpart:
                        pp.pprint((hwsubpart, hwfield, value))
                    

def memory_dict_transformer(memorydata):

    for hw, field in memorydata.items():
        for hwfield, value in field.items():
            print((hwfield, value))