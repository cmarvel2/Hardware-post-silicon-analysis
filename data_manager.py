import pandas as pd
import sqlite3
from System_data import Sysdata
from datetime import datetime

class Data_formatter:
    
    def __init__(self, system_data, process_data):
        self.system_data =  system_data
        self.process_data = process_data

    def System_telemetry_dataframe(self):
        df = pd.DataFrame(self.system_data)

        return df

    def processor_data_dataframe(self):
        df = pd.DataFrame(self.process_data)

        return df

system = Sysdata()
systemdata= system.get_telemetry()
processdata= system.get_top_processes()
formatteddata = Data_formatter(systemdata,processdata)
#print(formatteddata.System_telemetry_dataframe())
#print(formatteddata.processor_data_dataframe())


print(datetime.today())